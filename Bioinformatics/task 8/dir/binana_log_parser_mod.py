import argparse
import csv
import re
import logging


class Error(Exception):
    """ Class to raising exceptions. """
    pass


def get_com_line_args(logger):
    """ Function to get command line arguments. """
    logger.info("Getting command line arguments.")
    parser = argparse.ArgumentParser(
        description="Pure Python command line utility to get interatomic interactions.", add_help=True)

    parser.add_argument("--input_file", type=argparse.FileType(), help="Input log file path.", default="log.txt")
    parser.add_argument(
        "--out_txt", type=argparse.FileType(mode='w'), help="Output txt file path.")
    parser.add_argument(
        "--out_csv", type=argparse.FileType(mode='w'), help="Output csv file path.")

    return parser.parse_args()


def create_logger():
    """ Create logger function. """
    
    logger = logging.getLogger("binana_log_parser")
    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("binana_parser.log")
    
    c_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    return logger


# Hydrogen bonds:
# Hydrophobic contacts (C-C):
# pi-pi stacking interactions:
# T-stacking (face-to-edge) interactions:
# Cation-pi interactions:
# Salt Bridges:

amino_acids = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'CYS': 'C',
    'GLN': 'Q',
    'GLY': 'G',
    'GLU': 'E',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V'
}

BACKBONE = ['CA', 'C', 'O', 'N']

# For Hydrogen bonds output 
# ------------------------------------------------------------------------
superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

trans_tab = str.maketrans(
    ''.join(superscript_map.keys()),
    ''.join(superscript_map.values()))


def get_superscript_str(input_str):
    return input_str.translate(trans_tab)
# --------------------------------------------------------------------------


class Atom:
    """ Class Atom for storing the necessary atom information """
    atom_name = ''
    atom_writing_name = ''
    element = ''
    res_name = ''  # residue name
    res_num = 0  # residue number
    num_in_res = 0  # atom number in the residue
    chain = ''  # important only for Special case

    def print_atom(self):
        res_line = """Atom name: {} \nAtom writing name: {} \n
Element: {}\nResidue name: {}\nResidue number: {}\nNumber in residue: {}""".format(
            self.atom_name, self.element, self.atom_writing_name, self.res_name, self.res_num, self.num_in_res)
        print(res_line)

    def is_equal(self, atom2):
        """ Checks the difference between two atoms (important to Hydrogen interactions) """
        if self.atom_writing_name == atom2.atom_writing_name and \
                self.res_name == atom2.res_name and \
                self.res_num == atom2.res_num and \
                self.chain == atom2.chain:
            # if both of them are in amino acids
            if self.is_in_amino_acids() and atom2.is_in_amino_acids():
                # if both of them are backbone or both aren't backbone
                if not (self.is_back_bone() ^ atom2.is_back_bone()):
                    return True
            else:
                # if both of them are ligands (only for Standard case)
                if not self.is_in_amino_acids() ^ atom2.is_in_amino_acids():
                    return True
        return False

    def set_element(self):
        """ Sets an element by the name of the atom. !!! only for one letter elements """
        self.element = self.atom_name
        self.element = self.element.replace("0", "")
        self.element = self.element.replace("1", "")
        self.element = self.element.replace("2", "")
        self.element = self.element.replace("3", "")
        self.element = self.element.replace("4", "")
        self.element = self.element.replace("5", "")
        self.element = self.element.replace("6", "")
        self.element = self.element.replace("7", "")
        self.element = self.element.replace("8", "")
        self.element = self.element.replace("9", "")

        self.element = self.element[0:1].strip()

    def is_in_amino_acids(self):
        """ Checks if an atom belongs to the amino_acids """
        return self.res_name in amino_acids

    def is_back_bone(self):
        """ Checks if an atom belongs to backbone """
        if (
                self.atom_name.strip() == "CA"
                or self.atom_name.strip() == "C"
                or self.atom_name.strip() == "O"
                or self.atom_name.strip() == "N"
        ):
            return True
        else:
            return False

    def is_h_elem(self):
        """ Checks if an atom element is H """
        return self.element == 'H'


def split_atom(atom_str):
    """ Gets atom line like
        'C:GLY(316):H(3013)' or 'UNL(1):O(30)'
        and return an Atom object """
    atom = Atom()
    sub_str_list = re.split(r':', atom_str)
    # if there is a chain we set it, otherwise chain = '' (default value)
    if len(sub_str_list) == 3:
        atom.chain = sub_str_list[0]

    # print(atom_str)
    atom_str = sub_str_list[-1]
    res_str = sub_str_list[-2]

    atom.res_name = res_str[:3]  # first 3 symbols in res_str are residue name
    atom.res_num = res_str[4:-1]  # other symbols - residue number in ()
    # atom name is all symbols before (. It's true cause no atom names with ( symbol
    atom.atom_name = re.split(r'\(', atom_str)[0]
    # atom number in residue is only digits after ( symbol
    atom.num_in_res = re.search(r'\d+', re.split(r'\(', atom_str)[1]).group()

    atom.set_element()
    return atom


class InteractionsLines:
    """ Class for reading the source log file """
    h_bond_lines = []
    hydr_cont_lines = []
    pi_pi_lines = []
    t_stack_lines = []
    cat_pi_lines = []
    salt_bridg_lines = []
    atom_pair_four_lines = []
    
    num_h_bond = 0
    num_hydr_cont = 0
    num_pi_pi = 0
    num_t_stack = 0
    num_cat_pi = 0
    num_salt_bridg = 0
    
    # 'Standard' or 'Special' (the ligand is represented by amino acids) 
    lig_type = ''

    # Initializing interactions
    def __init__(self, raw_lines, logger):
        """ Gets log file lines and returns InteractionsLines object """
        logger.info("Getting information from input file.")
        # lines = [line.rstrip('\n ,') for line in raw_lines]
        lines = [line[:-1] for line in raw_lines]
        # print(lines)

        atom_pair_four_ind = lines.index("Atom-type pair counts within 4 angstroms:")
        ligand_atom_type_ind = lines.index("Ligand atom types:")

        h_bond_ind = lines.index("Hydrogen bonds:")
        halogen_ind = lines.index("Halogen bonds:")  # NOTE: added custom
        hydr_cont_ind = lines.index("Hydrophobic contacts (C-C):")
        pi_pi_ind = lines.index("pi-pi stacking interactions:")
        t_stack_ind = lines.index("T-stacking (face-to-edge) interactions:")
        cat_pi_ind = lines.index("Cation-pi interactions:")
        salt_bridg_ind = lines.index("Salt Bridges:")

        atom_pair_four_raw_ind = lines.index("Raw data:", atom_pair_four_ind, ligand_atom_type_ind)
        h_bond_raw_ind = lines.index("Raw data:", h_bond_ind, halogen_ind)  # NOTE: changed
        halogen_raw_ind = lines.index("Raw data:", halogen_ind, hydr_cont_ind)  # NOTE: added custom
        hydr_cont_raw_ind = lines.index("Raw data:", hydr_cont_ind, pi_pi_ind)
        pi_pi_raw_ind = lines.index("Raw data:", pi_pi_ind, t_stack_ind)
        t_stack_raw_ind = lines.index("Raw data:", t_stack_ind, cat_pi_ind)
        cat_pi_raw_ind = lines.index("Raw data:", cat_pi_ind, salt_bridg_ind)
        salt_bridg_raw_ind = lines.index("Raw data:", salt_bridg_ind)

        self.atom_pair_four_lines = [l.strip() for l in lines[atom_pair_four_raw_ind + 1: ligand_atom_type_ind - 1]]
        self.h_bond_lines = [l.strip() for l in lines[h_bond_raw_ind + 1: halogen_ind - 1]]  # NOTE: changed
        self.halogen_lines = [l.strip() for l in lines[halogen_raw_ind + 1: hydr_cont_ind - 1]]  # NOTE: added custom
        self.hydr_cont_lines = [l.strip() for l in lines[hydr_cont_raw_ind + 1: pi_pi_ind - 1]]
        self.pi_pi_lines = [l.strip() for l in lines[pi_pi_raw_ind + 1: t_stack_ind - 1]]
        self.t_stack_lines = [l.strip() for l in lines[t_stack_raw_ind + 1: cat_pi_ind - 1]]
        self.cat_pi_lines = [l.strip() for l in lines[cat_pi_raw_ind + 1: salt_bridg_ind - 1]]
        self.salt_bridg_lines = [l.strip() for l in lines[salt_bridg_raw_ind + 1:]]

        # print(self.atom_pair_four_lines)
        # print(lines[h_bond_raw_ind + 1: hydr_cont_ind - 1])

        self.num_h_bond = halogen_ind - h_bond_raw_ind - 2  # NOTE: changed
        self.num_halogen = hydr_cont_ind - halogen_raw_ind - 2  # NOTE: added custom
        self.num_hydr_cont = pi_pi_ind - hydr_cont_raw_ind - 2
        self.num_pi_pi = t_stack_ind - pi_pi_raw_ind - 2
        self.num_t_stack = salt_bridg_ind - cat_pi_raw_ind - 2
        self.num_cat_pi = cat_pi_ind - t_stack_raw_ind - 2
        self.num_salt_bridg = len(self.salt_bridg_lines)

    def is_interactions(self, logger):
        """ Checks for interactions """
        if self.num_h_bond + self.num_hydr_cont + \
            self.num_pi_pi + self.num_t_stack + \
                self.num_cat_pi + self.num_salt_bridg == 0:
            logger.error("The required interactions were not found. Check the file manually.")
            raise Error("The required interactions were not found.")
        else:
            return True

    def get_ligand_type(self, logger):
        """ Checks if ligand name in amino_acids and returns 'Standard' if no
            or 'Special' if yes and two chains are named differently """
        if self.num_hydr_cont:
            atoms = [item.strip() for item in re.split(r'-', self.hydr_cont_lines[0])]
        elif self.num_h_bond:
            atoms = [item.strip() for item in re.split(r'-', self.h_bond_lines[0])]
        elif self.num_pi_pi:
            atoms = [item.strip() for item in re.split(r'/', self.pi_pi_lines[0][1:-1])]
        elif self.num_t_stack:
            atoms = [item.strip() for item in re.split(r'/', self.t_stack_lines[0][1:-1])]
        elif self.num_cat_pi:
            atoms = [item.strip() for item in re.split(r'/', self.cat_pi_lines[0][1:-1])]
        elif self.num_salt_bridg:
            atoms = [item.strip() for item in re.split(r'/', self.salt_bridg_lines[0][1:-1])]
        lig_atom_parts = re.split(r':', atoms[0])
        rec_atom_parts = re.split(r':', atoms[-1])
        # checking if lig_name in amino_acid
        if lig_atom_parts[-2][:3] not in amino_acids:
            self.lig_type = 'Standard'
            logger.info("Ligand type is Standard.")
        else:
            if len(rec_atom_parts) != 3 or len(lig_atom_parts) != 3:
                logger.error("Ligand is represented by amino acids. And some chain hasn't got its name. \
                             Check it manually. Both chains must have their names. And they have to be different.")
                raise Error("Ligand is represented by amino acids. And some chain hasn't got its name.")
            else:
                if lig_atom_parts[0] == rec_atom_parts[0]:
                    logger.error("Ligand is represented by amino acids. And chains have the same names. \
                             Check it manually. Both chains must have different names.")
                    raise Error("Ligand is represented by amino acids. And chains have the same names.")
                else:
                    self.lig_type = 'Special'
                    logger.info("Ligand type is Special.")

    def check(self, logger):
        """ Checks if only one chain in receptor and in ligand.
            Checks if only one ligand name (only amino acids or just name) """
        lig_atoms = []
        rec_atoms = []
        
        for line in self.atom_pair_four_lines:
            atoms = [split_atom(item.strip()) for item in re.split(r'-', line)]
            lig_atoms.append(atoms[0])
            rec_atoms.append(atoms[1])
        lig_chain_name = lig_atoms[0].chain
        rec_chain_name = rec_atoms[0].chain
        
        for lig_atom in lig_atoms:
            if lig_atom.chain != lig_chain_name:
                logger.warning("Ligand is represented by more than one chain. Check the results manually.")
                return False
            if lig_atom.is_in_amino_acids() and self.lig_type == 'Standard' \
                    or not lig_atom.is_in_amino_acids() and self.lig_type == 'Special':
                logger.warning("Ligand is represented by more than one name (part). Check the results manually.")
                return False
        for rec_atom in rec_atoms:    
            if rec_atom.chain != rec_chain_name:
                logger.warning("Receptor is represented by more than one chain. Check the results manually.")         
                return False
        return True


# -------------------------------------------------------------------------------------------------
def get_amino_acid_letter(res_name, logger):
    """ Gets amino acid three letter name and returns amino acid one letter name.
        For non-amino acid residues (like ligands), returns the residue name as is. """
    if res_name in amino_acids:
        return amino_acids[res_name]
    else:
        # Instead of raising an error, return the residue name for non-amino acids
        return res_name
        

""" Functions for getting H-bond interactions """
# ----------------------------------------------------------------------------------------


def split_h_bond_line(h_bond_line, logger):
    """ Splits H-bond interaction line like
        'UNL(1):O(30) - C:GLY(316):H(3013) - C:GLY(316):N(3009)'
        and returns list of 3 atoms """
    atom_str_list = [item.strip() for item in re.split(r'-', h_bond_line)]

    # print(atom_str_list)

    if len(atom_str_list) != 3:
        logger.error("Hydrogen bond doesn't consist of 3 atoms")
        raise Error("Hydrogen bond doesn't consist of 3 atoms")
        
    h_bond_atoms = [split_atom(atom_str) for atom_str in atom_str_list]

    for atom in h_bond_atoms:        
        # set writing name (for output) for the first time 
        if atom.atom_name == atom.element or atom.is_h_elem():  # if the one-letter name or element is H
            atom.atom_writing_name = atom.element
        else:
            # !!! O23 - correct !!! for 2HH1 isn't working
            atom.atom_writing_name = atom.element + get_superscript_str(atom.atom_name[1:2])
    
    return h_bond_atoms     


def is_all_atoms_equal(atoms_mas1, atoms_mas2):
    """ Gets two lists of atoms and checks elementwise match  """
    mas = [atoms_mas1[i].is_equal(atoms_mas2[i]) for i in range(3)]
    return all(mas)


def get_repeat_h_lines(h_atoms):
    """ Get all H-bond interactions atoms (matrix n*3) and
        returns list of lists with repeated lines"""
    mas_repeat_h = []
    check = [False for i in range(len(h_atoms))]

    for i in range(len(h_atoms)):
        if not check[i]:
            mas = [i]
            for j in range(i+1, len(h_atoms)):
                if not check[j]:
                    if is_all_atoms_equal(h_atoms[i], h_atoms[j]):
                        mas.append(j)
                        check[j] = True
            mas_repeat_h.append(mas)            

    return mas_repeat_h


# !!! we change only first ligand atom name.
# doesn't affect the special case (cause output without digits) 
def extension_atom_writing_name(mas_index, h_atoms, logger):
    """ Gets list of identical lines indexes and 
        adds one character to the current name of the first atom """
    
    for ind in mas_index:
        prev_writ_name = h_atoms[ind][0].atom_writing_name
        atom_name = h_atoms[ind][0].atom_name
        if len(prev_writ_name) < len(atom_name):
            h_atoms[ind][0].atom_writing_name = prev_writ_name + \
                get_superscript_str(atom_name[len(prev_writ_name):len(prev_writ_name)+1])
        else:
            logger.warning("Index out of range. Maybe, two identical H-bond interactions lines was found. \
                            Or it's length difference in their first atoms names. Check manually.")
        # in case above we use 'if else' (not 'try except') cause of a length difference like CA-H-N and C-H-N
    return h_atoms


def is_all_unique(rep_h_lines):
    """ Checks if all atoms are different """
    for mas_ind in rep_h_lines:
        if len(mas_ind) > 1:
            return False
    else:
        return True
    
    
def do_all_unique(h_bond_lines, logger):
    """ Gets all H-bond interactions lines and makes their output unique """
    # print(h_bond_lines)
    h_atoms = [split_h_bond_line(h_bond_line, logger) for h_bond_line in h_bond_lines]
    
    count = 0
    while True:
        
        if count > 5:  # the longest name consist of 4 letters
            logger.error("Looping. Two identical lines was founded. Check it manually.")
            raise Error("Two identical lines was founded. Check it manually.")
        rep_h_lines = get_repeat_h_lines(h_atoms)
        if is_all_unique(rep_h_lines):
            break
        else:
            count += 1
            for mas_ind in rep_h_lines:
                if len(mas_ind) > 1:
                    extension_atom_writing_name(mas_ind, h_atoms, logger)
    return h_atoms


def get_h_bond_res_line_special(h_bond_atoms):
    """ Get list of 3 atoms and returns the resulting line
        for one H-bond interaction (Special case)"""
    res_line = f''
    # first atom always atom from ligand and is not H
    
    first_atom = h_bond_atoms[0]
    second_atom = h_bond_atoms[1]
    third_atom = h_bond_atoms[2]
    
    # !!! not writing name
    res_line += f'{first_atom.element}'
    
    # if first and second atoms are ligand
    if first_atom.chain == second_atom.chain:
        res_line += second_atom.element  # second atom always H
        res_line += f'[{get_amino_acid_letter(first_atom.res_name, logger)}{first_atom.res_num}]'
        if first_atom.is_back_bone():
            res_line += '*'
        else:
            res_line += '**'
        res_line += '...'
        if third_atom.is_back_bone():
            res_line += '*'
            res_line += third_atom.element
        else:
            res_line += '**'
            res_line += third_atom.element

    else:
        res_line += f'[{get_amino_acid_letter(first_atom.res_name, logger)}{first_atom.res_num}]'
        if first_atom.is_back_bone():
            res_line += '*'
        else:
            res_line += '**'
        res_line += '...'
        if third_atom.is_back_bone():
            res_line += '*'
            res_line += second_atom.element + third_atom.element
        else:
            res_line += '**'
            res_line += second_atom.element + third_atom.element
        
    res_line += f'[{get_amino_acid_letter(third_atom.res_name, logger)}{third_atom.res_num}]'
    return res_line


def get_h_bond_res_line_standard(h_bond_atoms):
    """ Gets list of 3 atoms and returns the resulting line
        for one H-bond interaction (Standard case)"""
    
    res_line = f''
    # first atom always atom from ligand and is not H
    
    first_atom = h_bond_atoms[0]
    second_atom = h_bond_atoms[1]
    third_atom = h_bond_atoms[2]
    
    res_line += f'{first_atom.atom_writing_name}'
    
    if second_atom.is_in_amino_acids():
        # if receptor
        res_line += '...'
        # check third atom is in backbone or side chain
        if third_atom.is_back_bone():
            res_line += '*'
            res_line += second_atom.element + third_atom.element
        else:
            res_line += '**'
            res_line += second_atom.element + third_atom.element
    else:
        # assume that the second atom is always H
        res_line += second_atom.element
        res_line += '...'
        # check third atom is in backbone or side chain
        if third_atom.is_back_bone():
            res_line += '*'
            res_line += third_atom.element
        else:
            res_line += '**'
            res_line += third_atom.element
    
    res_line += f'[{get_amino_acid_letter(third_atom.res_name, logger)}{third_atom.res_num}]'
    return res_line 


def get_h_bond_result(h_bond_lines, lig_type, logger):
    """ Returns the resulting string for all H-bond interactions """
    # print(h_bond_lines)
    logger.info('Parsing of Hydrogen bonds.')
    result = ''
    h_atoms = do_all_unique(h_bond_lines, logger)
    if lig_type == 'Standard':
        for h_line_atoms in h_atoms:
            result += get_h_bond_res_line_standard(h_line_atoms) + ', '   
    else:
        for h_line_atoms in h_atoms:
            result += get_h_bond_res_line_special(h_line_atoms) + ', ' 
    return result[:-2] 


""" Functions for getting hydrophobic interactions """
# --------------------------------------------------------------------


def get_hydr_cont_residue(hydr_cont_line, logger):
    """ Gets hydrophobic contacts line like
        ATP(1):C39(3) - A:TYR(58):CD2(67) and returns 
        amino acid with its number like Y58 or ligand name like ATP1 """
    parts = hydr_cont_line.split(' - ')
    # Check if we're dealing with the receptor part (amino acid)
    residue = re.split(r':', parts[1])[-2]
    res_name = residue[:3]
    res_num = re.search(r'\d+', residue).group()
    
    if res_name in amino_acids:
        # For amino acids, use one-letter code
        sub_res = '{}{}'.format(get_amino_acid_letter(res_name, logger), res_num)
    else:
        # For non-amino acids (ligands), use full name
        sub_res = '{}{}'.format(res_name, res_num)
    
    return sub_res


def get_hydr_contacts_result(hydr_cont_lines, logger):
    """ Returns the resulting line for hydrophobic contacts """ 
    logger.info("Parsing of Hydrophobic contacts.")
    residues = {}
    result = ''
    for hydr_cont_line in hydr_cont_lines:
        res = get_hydr_cont_residue(hydr_cont_line, logger)
        if res in residues:
            residues[res] += 1
        else:
            residues[res] = 1

    for residue, count in residues.items():
        result += '{}({}), '.format(residue, count)
    return result[:-2] 


# ------------------------------------------------------------------------------
# suitable for 4 types of interactions
def get_atoms_from_line(salt_sub_line):
    """ Gets sub line like
        ATP(1):PA(8) / ATP(1):O59(7) / ATP(1):O2A(9) / ATP(1):O1A(10) / ATP(1):O3A(11)
        returns ligand / receptor atoms list """ 
    atoms = [split_atom(atom_str.strip()) for atom_str in re.split(r'/', salt_sub_line)]
        
    return atoms


def get_amino_acid_str(line, lig_type):
    """ Gets salt bridges / pi-pi / cation-pi / t-stacking line like
        [ATP(1):PA(8) / ATP(1):O59(7) / ATP(1):O2A(9) / ATP(1):O1A(10) / ATP(1):O3A(11)] 
        - [A:LYS(87):NZ(345) / A:LYS(87):HZ1(346) / A:LYS(87):HZ2(347) / A:LYS(87):HZ3(348)]
        and returns amino acid with its number like 'K87' or 'LIG1 - K87' """
    sub_lines = [s.strip()[1:-1] for s in re.split(r'-', line)]

    if len(sub_lines) < 2:
        return None

    rec_atom = get_atoms_from_line(sub_lines[1])[0]
    lig_atom = get_atoms_from_line(sub_lines[0])[0]
    
    if lig_type == 'Standard':
        # For standard case, just show the receptor residue
        if rec_atom.res_name in amino_acids:
            res = f'{get_amino_acid_letter(rec_atom.res_name, logger)}{rec_atom.res_num}'
        else:
            res = f'{rec_atom.res_name}{rec_atom.res_num}'
    else:
        # For special case, show both ligand and receptor
        lig_part = f'{get_amino_acid_letter(lig_atom.res_name, logger)}{lig_atom.res_num}'
        rec_part = f'{get_amino_acid_letter(rec_atom.res_name, logger)}{rec_atom.res_num}'
        res = f'{lig_part} - {rec_part}'
    
    return res


def get_amino_acids_result(lines, lig_type, inter_str, logger):
    """ Gets all salt bridges / pi-pi / cation-pi / t-stacking lines
        and returns the resulting output string for them  """
    logger.info(f'Parsing of {inter_str} lines.')
    
    residues = {}
    result = ''
    for line in lines:
        # print(line, lig_type)
        res = get_amino_acid_str(line, lig_type)
        if res in residues:
            residues[res] += 1
        else:
            residues[res] = 1

    for res, count in residues.items():
        if count > 1:
            result += f'{res}({count}), '
        else:
            result += f'{res}, '
    return result[:-2] 


if __name__ == "__main__":
    logger = create_logger()

    args = get_com_line_args(logger)

    print('*******************************************\n')
    print(f'Start processing of file: {args.input_file}\n')

    log_lines = args.input_file.readlines()
    # print(log_lines)
    interactions = InteractionsLines(log_lines, logger)
    interactions.is_interactions(logger)
    interactions.get_ligand_type(logger)
    interactions.check(logger)
    res_list = []

    # Hydrogen bonds:
    res_list.append(get_h_bond_result(interactions.h_bond_lines, interactions.lig_type, logger))
    # Hydrophobic contacts (C-C):
    res_list.append(get_hydr_contacts_result(interactions.hydr_cont_lines, logger))
    # pi-pi stacking interactions:
    inter_str = 'pi-pi'
    res_list.append(get_amino_acids_result(interactions.pi_pi_lines, interactions.lig_type, inter_str, logger))
    # T-stacking (face-to-edge) interactions:
    inter_str = 't-stacking'
    res_list.append(get_amino_acids_result(interactions.t_stack_lines, interactions.lig_type, inter_str, logger))
    # Cation-pi interactions:
    inter_str = 'cation-pi'
    res_list.append(get_amino_acids_result(interactions.cat_pi_lines, interactions.lig_type, inter_str, logger))
    # Salt Bridges:
    inter_str = 'salt bridges'
    res_list.append(get_amino_acids_result(interactions.salt_bridg_lines, interactions.lig_type, inter_str, logger))
    headers = ["Hydrogen bonds", "Hydrophobic contacts (C-C)", "pi-pi stacking interactions",
               "T-stacking (face-to-edge) interactions", "Cation-pi interactions", "Salt Bridges"]  # NOTE: added

    if args.out_csv:
        writer = csv.writer(args.out_csv)
        writer.writerow(headers)
        writer.writerow(res_list)

    if args.out_txt:
        for ind, header in enumerate(headers):
            args.out_txt.write(f'{header}: {res_list[ind]}\n\n')

    if not args.out_csv and not args.out_txt:
        with open("output.txt", 'w') as f:
            for ind, header in enumerate(headers):
            	f.write(f'{header}: {res_list[ind]}\n\n')

    print(f'End processing of file: {args.input_file}')
    print('\n*******************************************\n')
