package Views;



import javax.swing.*;
import java.awt.*;

public class MainGUI extends JFrame {
    JFrame frame;
    JPanel panel;
    JButton enterButton;
    JButton exitButton;
    JLabel infoText;
    GridBagConstraints gbc = new GridBagConstraints();



    public MainGUI() {
        frame = new JFrame("Main");
        panel = new JPanel(new GridBagLayout());
        infoText = new JLabel("you are not close to parking entry");

        panel.add(infoText);
        frame.setSize(300, 200);
        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        frame.setResizable(false);




    }

    public JFrame enter() {
        enterButton = new JButton("Enter");
        gbc.gridx = 0;
        gbc.gridy = 4;
        gbc.gridwidth = 3;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(enterButton, gbc);
        return frame;


    }

    public JFrame pay() {
        exitButton = new JButton("Pay");
        gbc.gridx = 2;
        gbc.gridy = 5;
        gbc.gridwidth = 3;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(exitButton, gbc);
        return frame;
    }





    public JFrame getFrame() {
        return frame;
    }


    public JPanel getPanel() {
        return panel;
    }

    public JButton getEnterButton() {
        return enterButton;
    }

    public JButton getExitButton() {
        return exitButton;
    }




}