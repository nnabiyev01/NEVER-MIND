import Controllers.UserController;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;


public class Server implements Runnable {
    Socket socket;

    private static final String USERSFILE = "users.txt";

    /**
     * socket connection of current client
     *
     * @param socket socket connection
     */
    public Server(Socket socket) {
        this.socket = socket;
    }

    public void run() {
        System.out.printf("Connection received from %s\n", socket);

        UserController userController = new UserController(USERSFILE);


        try {
            Scanner in = new Scanner(socket.getInputStream());
            PrintWriter pw = new PrintWriter(socket.getOutputStream());
            String[] parameters;
            String parameter;
            String name;
            String password;
            String response;
            Boolean responseBoolean;

            while (in.hasNextLine()) {

                String requestLine = in.nextLine();

                switch (requestLine) {
                    // All user related actions
                    case "/SignUp":
                        // InputFromClient: name|password
                        // Response : true or false| User or Reason
                        parameters = in.nextLine().replace(",", "\\,/").split("\\|");
                        name = parameters[0];
                        password = parameters[1];
                        String licensePlate = parameters[2];

                        response = userController.createAccount(name, password, licensePlate);
                        pw.println(response);
                        break;

                    case "/Login":
                        // InputFromClient: name|password
                        // Response : True or False| User or Reason
                        parameters = in.nextLine().replace(",", "\\,/").split("\\|");
                        name = parameters[0];
                        password = parameters[1];

                        response = userController.loginUser(name, password);
                        pw.println(response);
                        break;

                    case "/EditUser":
                        // InputFromClient: UserName|newPassword
                        // Response : True or False
                        parameters = in.nextLine().replace(",", "\\,/").split("\\|");
                        responseBoolean = userController.editUser(parameters[0], parameters[1]);
                        pw.println(responseBoolean);

                        break;

                    case "/DeleteUser":
                        //InputFromClient: UserName
                        // Response : True or False
                        parameter = in.nextLine().replace(",", "\\,/");
                        responseBoolean = userController.deleteUser(parameter);
                        pw.println(responseBoolean);
                        break;


                    // All Posts related action




                    default:
                        pw.println("Error 404");
                }
                pw.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        createFilesIfNotExists(USERSFILE);

        // allocate server socket at given port
        try {
            // waiting for clients to connect
            ServerSocket serverSocket = new ServerSocket(4444);
            System.out.printf("socket open, connect on %s\n", serverSocket);

            // infinite loop to accept multiple connection
            while (true) {
                // accepting a client connection
                Socket socket = serverSocket.accept();
                // initializing instance of a class with the current socket
                Server server = new Server(socket);
                // spawn thread to handle each client
                new Thread(server).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void createFilesIfNotExists(String filename) {
        File file = new File(filename);
        if (!file.isFile()) {
            try {
                if (file.createNewFile())
                    System.out.println(filename + "file created");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}