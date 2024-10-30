import javax.swing.*;
import java.awt.*;
import java.io.File;

public class Run {

    public static String pathToRules = "/Users/leonid/Desktop/GitHub/course_4/Arti Intelligense/task 1/rules.txt";
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame();
            try {
                UIManager.setLookAndFeel(
                        UIManager.getSystemLookAndFeelClassName());

            } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException e) {
                e.printStackTrace();
            }
            initFrameDim(frame);
            StartAction startAction = new StartAction();
            initApplication(frame, startAction, WindowConstants.EXIT_ON_CLOSE);
        });
    }

    private static void initFrameDim(JFrame frame) {
        Dimension screen = Toolkit.getDefaultToolkit().getScreenSize();
        frame.setSize(400, (int) (screen.getHeight() * .5));
        frame.setLocation(screen.width/2 - frame.getSize().width/2, screen.height/2 - frame.getSize().height/2);
        frame.setResizable(true);
    }

    private static void initApplication(JFrame frame, StartAction startAction, final int onCloseOperation) {
        frame.setTitle("МАШИНА " +
                "ДЕДУКТИВНОГО " +
                "ВЫВОДА");
        frame.setDefaultCloseOperation(onCloseOperation);
        frame.getContentPane().add(startAction.getMasterComponent(), BorderLayout.CENTER);
        JPanel panel = new JPanel();
        JButton openFile = new JButton("Open File");
        JButton start = new JButton("Start");

        openFile.addActionListener(e -> {
            JFileChooser chooser = new JFileChooser();
            chooser.setCurrentDirectory(new File("/Users/leonid/Desktop/GitHub/course_4/Arti Intelligense/task 1"));
            int returnVal = chooser.showOpenDialog(frame);
            if(returnVal == JFileChooser.APPROVE_OPTION) {
                System.out.println("You chose to open this file: " +
                        chooser.getSelectedFile().getAbsolutePath());
                pathToRules = chooser.getSelectedFile().getAbsolutePath();
            }
        });

        start.addActionListener(startAction);
        panel.add(openFile);
        panel.add(start);
        frame.getContentPane().add(panel, BorderLayout.SOUTH);
        frame.setVisible(true);
    }
    
}
