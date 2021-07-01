import Views.*;
import com.sun.tools.javac.Main;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.io.*;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;


public class Client implements ActionListener, MouseListener, Runnable {
    StarterPage starterPage;
    LoginGUI loginGUI;
    SignUpGUI signUpGUI;
    String username;
    String password;
    MainGUI mainGUI;
    boolean start = true;
    private static Scanner in;
    private static PrintWriter pw;

    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 4444);
            in = new Scanner(socket.getInputStream());
            pw = new PrintWriter(socket.getOutputStream());

            SwingUtilities.invokeLater(new Client());
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void run() {
        //initialize main GUIs
        starterPage = new StarterPage();
        loginGUI = new LoginGUI();
        signUpGUI = new SignUpGUI();
        if (start) {
            mainGUI = new MainGUI();

            System.out.print("entered");

        }

        //Buttons
        //Starter Page
        starterPage.getLoginButton().addActionListener(this);
        starterPage.getSignUpButton().addActionListener(this);

        // From Login
        loginGUI.getLoginButton().addActionListener(this);
        loginGUI.getHyperlink().addMouseListener(this);

        // From SignUp
        signUpGUI.getSignUpButton().addActionListener(this);
        signUpGUI.getHyperlink().addMouseListener(this);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == starterPage.getLoginButton()) {
            System.out.println("Login button in starter page clicked");

            starterPage.getFrame().setVisible(false);
            loginGUI.getFrame().setVisible(true);

        }

        if (e.getSource() == starterPage.getSignUpButton()) {
            System.out.println("Sign up button in starter page clicked");

            starterPage.getFrame().setVisible(false);
            signUpGUI.getFrame().setVisible(true);

        }

        /* Sign Up Screen */
        // Sign up button in sign up screen


        if (e.getSource() == signUpGUI.getSignUpButton()) {
            signUpButtonAction();
        }

        /* Login screen */
        //Login
        if (e.getSource() == loginGUI.getLoginButton()) {
            loginButtonAction();
        }
    }


    @Override
    public void mouseClicked(MouseEvent e){
        if (e.getSource() == loginGUI.getHyperlink()) {
            System.out.println("Sign up button in login page clicked");

            loginGUI.getFrame().dispose();
            signUpGUI.getFrame().setVisible(true);
        }

        if (e.getSource() == signUpGUI.getHyperlink()) {
            System.out.println("Login button in sign up page clicked");

            signUpGUI.getFrame().dispose();
            loginGUI.getFrame().setVisible(true);
        }
    }

    private void signUpButtonAction() {
        if (!signUpGUI.getPasswordText().getText().equals(signUpGUI.getConfirmPasswordSignUp().getText())) {
            JOptionPane.showMessageDialog(null, "passwords do not match",
                    "Sign Up Error", JOptionPane.ERROR_MESSAGE);
            signUpGUI.getPasswordText().setText("");
            signUpGUI.getConfirmPasswordSignUp().setText("");
        } else {
            String usernameCreate;
            usernameCreate = signUpGUI.getUsernameText().getText();
            System.out.println("Username created! " + usernameCreate);

            String passwordCreate;
            passwordCreate = String.valueOf(signUpGUI.getPasswordText().getPassword());
            System.out.println("Password created! " + passwordCreate);

            String licensePLate = signUpGUI.getLicensePlateLogin().getText();
            // checking if empty
            if (passwordCreate.isEmpty() || usernameCreate.isEmpty()) {
                JOptionPane.showMessageDialog(null, "Empty Field",
                        "Sign Up Error", JOptionPane.ERROR_MESSAGE);
            } else {

                // sending the data to server
                pw.println("/SignUp");
                pw.println(usernameCreate + "|" + passwordCreate + "|" + licensePLate);
                pw.flush();

                String[] response = in.nextLine().split("\\|");
                boolean responseBool = Boolean.parseBoolean(response[0]);
                if (responseBool) {
                    // SIGNUP SUCCESSFUL
                    String[] user = response[1].split(", ");
                    JOptionPane.showMessageDialog(null, "Your account has been created as " +
                                    user[0].replace("\\,/", ","),
                            "Welcome", JOptionPane.INFORMATION_MESSAGE);
                    username = user[0].replace("\\,/", ",");
                    password = user[1].replace("\\,/", ",");
                    mainGUI.getFrame().setVisible(true);

                } else {
                    JOptionPane.showMessageDialog(null, response[1],
                            "Welcome", JOptionPane.ERROR_MESSAGE);
                    // Clear all text fields in Signup GUI
                    signUpGUI.getUsernameText().setText("");
                    signUpGUI.getPasswordText().setText("");
                    signUpGUI.getConfirmPasswordSignUp().setText("");
                }
            }
        }
    }

    private void loginButtonAction() {
        System.out.println("Login button clicked");

        String usernameTyped = loginGUI.getUsernameLogin().getText();
        String passwordTyped = loginGUI.getPasswordLogin().getText();
        System.out.println("Username: " + usernameTyped);
        System.out.println("Password: " + passwordTyped);


        // checking if empty
        if (passwordTyped.isEmpty() || usernameTyped.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Empty Field",
                    "Sign Up Error", JOptionPane.ERROR_MESSAGE);
        } else {

            // sending the data to server
            pw.println("/Login");
            pw.println(usernameTyped + "|" + passwordTyped);
            pw.flush();

            // receiving response
            String[] response = in.nextLine().split("\\|");
            boolean responseBool = Boolean.parseBoolean(response[0]);
            if (responseBool) {
                // LOGIN SUCCESSFUL
                String[] user = response[1].split(", ");
                JOptionPane.showMessageDialog(null, "Welcome Back " + user[0].replace("\\,/", ","),
                        "Welcome", JOptionPane.INFORMATION_MESSAGE);
                username = user[0].replace("\\,/", ",");
                password = user[1].replace("\\,/", ",");
                loginGUI.getUsernameLogin().setText("");
                loginGUI.getPasswordLogin().setText("");
                loginGUI.getFrame().setVisible(false);
                mainGUI.getFrame().setVisible(true);

            } else {
                JOptionPane.showMessageDialog(null, response[1],
                        "Welcome", JOptionPane.ERROR_MESSAGE);
                // Clear all text fields in Login GUI
                loginGUI.getUsernameLogin().setText("");
                loginGUI.getPasswordLogin().setText("");

            }
        }
    }




    @Override
    public void mousePressed(MouseEvent e) {

    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }



}


