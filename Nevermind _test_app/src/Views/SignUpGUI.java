package Views;

import javax.swing.*;
import java.awt.*;


public class SignUpGUI extends JFrame {
    JFrame frame;
    JPanel panel;
    JTextField usernameSignUp;
    JPasswordField passwordSignUp;
    JPasswordField confirmPasswordSignUp;
    JTextField licensePlateLogin;
    JButton signUpButton;
    JLabel goToLogin;

    public SignUpGUI() {
        frame = new JFrame("Sign Up");
        panel = new JPanel(new GridBagLayout());

        GridBagConstraints gbc = new GridBagConstraints();
        JLabel usernameLabel = new JLabel("Username: ");
        gbc.gridx = 0;
        gbc.gridy = 0;
        panel.add(usernameLabel, gbc);

        usernameSignUp = new JTextField(10);
        gbc.gridx = 1;
        gbc.gridy = 0;
        panel.add(usernameSignUp, gbc);

        JLabel plateLabel = new JLabel("PlateNumber: ");
        gbc.gridx = 0;
        gbc.gridy = 1;
        panel.add(plateLabel, gbc);

        licensePlateLogin = new JTextField(10);
        gbc.gridx = 1;
        gbc.gridy = 1;
        panel.add(licensePlateLogin, gbc);



        JLabel passwordLabel = new JLabel("Password: ");
        gbc.gridx = 0;
        gbc.gridy = 2;
        panel.add(passwordLabel, gbc);

        passwordSignUp = new JPasswordField(10);
        gbc.gridx = 1;
        gbc.gridy = 2;
        panel.add(passwordSignUp, gbc);

        JLabel confirmPasswordLabel = new JLabel("Confirm Password: ");
        gbc.gridx = 0;
        gbc.gridy = 3;
        panel.add(confirmPasswordLabel, gbc);

        confirmPasswordSignUp = new JPasswordField(10);
        gbc.gridx = 1;
        gbc.gridy = 3;
        panel.add(confirmPasswordSignUp, gbc);



        signUpButton = new JButton("Sign Up");
        gbc.gridx = 0;
        gbc.gridy = 4;
        gbc.gridwidth = 3;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(signUpButton, gbc);

        goToLogin = new JLabel("Already have an account?");
        goToLogin.setFont(new Font("Arial", Font.ITALIC, 10));
        goToLogin.setForeground(Color.BLUE.darker());
        goToLogin.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        gbc.gridx = 0;
        gbc.gridy = 5;
        gbc.gridwidth = 3;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(goToLogin, gbc);

        frame.setSize(300, 200);
        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        frame.setResizable(false);
    }

    public JFrame getFrame() {
        return frame;
    }

    public JPanel getPanel() {
        return panel;
    }

    public JTextField getUsernameText() {
        return usernameSignUp;
    }


    public JTextField getLicensePlateLogin() {
        return licensePlateLogin;
    }




    public JPasswordField getPasswordText() {
        return passwordSignUp;
    }

    public JPasswordField getConfirmPasswordSignUp() {
        return confirmPasswordSignUp;
    }

    public JButton getSignUpButton() {
        return signUpButton;
    }

    public JLabel getHyperlink() {
        return goToLogin;
    }
}