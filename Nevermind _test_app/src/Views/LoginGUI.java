package Views;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class LoginGUI extends JFrame {
    JFrame frame;
    JPanel panel;
    JTextField usernameLogin;
    JPasswordField passwordLogin;
    JButton loginButton;
    JTextField licensePlateLogin;
    JLabel goToSignUp;


    public LoginGUI() {
        frame = new JFrame("Login");
        panel = new JPanel(new GridBagLayout());

        GridBagConstraints gbc = new GridBagConstraints();
        JLabel usernameLabel = new JLabel("Username: ");
        gbc.gridx = 0;
        gbc.gridy = 0;
        panel.add(usernameLabel, gbc);

        usernameLogin = new JTextField(10);
        gbc.gridx = 1;
        gbc.gridy = 0;
        panel.add(usernameLogin, gbc);

        JLabel passwordLabel = new JLabel("Password: ");
        gbc.gridx = 0;
        gbc.gridy = 1;
        panel.add(passwordLabel, gbc);


        passwordLogin = new JPasswordField(10);
        gbc.gridx = 1;
        gbc.gridy = 1;
        panel.add(passwordLogin, gbc);


        loginButton = new JButton("Login");
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 3;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(loginButton, gbc);

        goToSignUp = new JLabel("Don't have an account?");
        goToSignUp.setFont(new Font("Arial", Font.ITALIC, 10));
        goToSignUp.setForeground(Color.BLUE.darker());
        goToSignUp.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.gridwidth = 3;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(goToSignUp, gbc);

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

    public JTextField getUsernameLogin() {
        return usernameLogin;
    }

    public JPasswordField getPasswordLogin() {
        return passwordLogin;
    }

    public JButton getLoginButton() {
        return loginButton;
    }

    public JLabel getHyperlink() {
        return goToSignUp;
    }
}
