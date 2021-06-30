package Views;


import Controllers.UserController;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;


public class StarterPage extends JFrame {
    JFrame frame;
    JPanel panel;
    JButton loginButton;
    JButton signUpButton;

    public StarterPage() {
        frame = new JFrame("Login or Sign Up");
        panel = new JPanel(null);

        loginButton = new JButton("Login");
        loginButton.setBounds(15, 20, 260, 50);
        panel.add(loginButton);

        signUpButton = new JButton("Sign Up");
        signUpButton.setBounds(15, 85, 260, 50);
        panel.add(signUpButton);

        frame.setSize(300, 200);
        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        frame.setResizable(false);
        frame.setVisible(true);
    }

    public JFrame getFrame() {
        return frame;
    }

    public JPanel getPanel() {
        return panel;
    }

    public JButton getLoginButton() {
        return loginButton;
    }

    public JButton getSignUpButton() {
        return signUpButton;
    }
}
