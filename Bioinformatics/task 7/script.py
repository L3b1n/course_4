# -*- coding: utf-8 -*-
#import argparse
from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import glob
import subprocess
import os
#print(os.listdir(os.path.join(os.getcwd(), '..', '..', '..', 'bio/qvina/bin')))
#print(os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'bio/qvina/bin/vina')))


#def parse_args():
#    parser = argparse.ArgumentParser(description=u'Запускной скрип для Autodock Vina и его клонов')
#    parser.add_argument('dock_file', help=u'Исполняемый файл программы Autodock Vina', type=str)
#    parser.add_argument('--cpu', '-c', help=u'Количество задействованных ядер процессора. '
#                                                  u'По умолчанию будут использованы все.', type=int)
#    parser.add_argument('-r', '--receptor', help=u'Рецептор-мишень для докинга. По умолчанию за мишень принимается '
#                                                 u'файл rec.pdbqt.', type=str, default='rec.pdbqt')
#    parser.add_argument('-l', '--ligands', help=u'Каталог с лигандами для докинга в формате pdbqt. По умолчанию за каталог мишеней '
#                                               u'принимается ligands/', type=str, default='ligands/')
#    parser.add_argument('-f', '--config', help=u'Конфигурационный файл для докинга. По умолчанию - rec.conf', type=str, default='rec.conf')
#    parser.add_argument('-p', '--prefix', help=u'Префикс. По умолчанию - out', type=str, default='out')
#
#    return parser.parse_args()
#DOCK_FILE = os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'bio/qvina/bin/qvina')) 
DOCK_FILE = '~/Downloads/autodock_vina_1_1_2_mac_catalina_64bit/bin/vina'
CPU = 1
RECEPTOR = './RECEPTOR_ABL_mut/'
LIGANDS = './ligands_ABL_mut/'
CONFIG = 'ABL_mutant.txt'
PREFIX = 'OUT_ABL_mutant'

def worker(work_queue, done_queue):
    try:
        for ligand in iter(work_queue.get, 'STOP'):
            status_code = single_dock(ligand)
            done_queue.put("%s - %s %s." % (current_process().name, ligand, status_code))
    except Exception, e:
        done_queue.put("%s failed on %s with: %s" % (current_process().name, ligand, e.message))
    return True


def main():
    #args = parse_args()
    ligands = glob.iglob(LIGANDS+'*.pdbqt')
    try:
        os.stat(PREFIX)
    except:
        os.mkdir(PREFIX)
    workers = CPU or cpu_count()
    work_queue = Queue()
    done_queue = Queue()
    processes = []

    for ligand in ligands:
        work_queue.put(ligand)

    for w in xrange(workers):
        p = Process(target=worker, args=(work_queue, done_queue))
        p.start()
        processes.append(p)
        work_queue.put('STOP')

    for p in processes:
        p.join()

    done_queue.put('STOP')

    for status in iter(done_queue.get, 'STOP'):
        print status


def single_dock(ligand):
    li = os.path.basename(ligand).split('.')[0]
    try:
        os.stat(PREFIX+'/'+li)
	if os.path.isfile('{0}/{1}/{1}_s.pdbqt'.format(PREFIX,li)) and os.path.isfile('{0}/{1}/{1}_log.txt'.format(PREFIX,li)):
		return "complite"
    except:
        os.mkdir(PREFIX+'/'+li)
    cmd = '{0} --config {1} --ligand {2} --out {3}/{4}/{4}_s.pdbqt --log {3}/{4}/{4}_log.txt'.format(DOCK_FILE, CONFIG, ligand, PREFIX, li)
    stdout = subprocess.call(cmd, shell=True)
    return "complite"

if __name__ == '__main__':
    main()
