package Controllers;


import Models.User;


import java.io.*;
import java.util.ArrayList;

public class UserController {
    private final String filename;

    public UserController(String filename) {
        this.filename = filename;
    }

    //Create new account
    public String createAccount(String username, String password, String licensePlate) {
        String result = "false|Error";
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line = br.readLine();
            while (line != null) {
                // edge case for an empty file or line
                if (line.equals("")) {
                    line = br.readLine();
                    continue;
                }
                String[] components = line.split(", ");
                // checking if user name exists
                if (components[0].equals(username)) {
                    result = "false|user already exists";
                    return result;
                }
                line = br.readLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        try (PrintWriter pw = new PrintWriter(new FileWriter(filename, true))) {
            User user = new User(username, password, licensePlate);
            pw.println(user.toString());
            result = String.format("true|%s", user.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }

        return result;
    }

    //Check password
    public String loginUser(String username, String password) {
        String result = "false|UserDoesNotExist";
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line = br.readLine();
            while (line != null) {
                // edge case for an empty file or line
                if (line.equals("")) {
                    line = br.readLine();
                    continue;
                }
                String[] components = line.split(", ");
                // if username and password match
                if (components[0].equals(username)) {
                    if (components[1].equals(password))
                        result = "true|" + line;
                    else
                        result = "false|Incorrect Password";
                    break;
                }
                line = br.readLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
            result = "false|Error";
        }

        return result;
    }


    public boolean editUser(String userName, String newPassword) {
        String oldContent = "";

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line = br.readLine();
            ArrayList<String> lines = new ArrayList<>();


            while (line != null) {
                // edge case for an empty file or line
                if (line.equals("")) {
                    line = br.readLine();
                    continue;
                }
                lines.add(line);
                line = br.readLine();
            }


            br.close();
            FileWriter writer = new FileWriter(filename);


            boolean flag = false;
//            FileWriter writer = new FileWriter(filename);
            for (int i = 0; i < lines.size(); i++) {
                String[] components = lines.get(i).split(", ");
                if (components[0].equals(userName)) {
                    User user = new User(components[0], components[1], components[2]);
                    user.setPassword(newPassword);
                    String newContent = user.toString() + System.lineSeparator();
                    writer.write(newContent);
                    flag = true;


                } else {
                    oldContent = lines.get(i) + System.lineSeparator();
                    writer.write(oldContent);

                }

            }

            writer.close();
            return flag;


        } catch (IOException e) {
            e.printStackTrace();
        }

        return false;
    }

    //Delete account
    public boolean deleteUser(String userName) {
        boolean flag = false;
        try {
            ArrayList<String> lines = new ArrayList<>();
            String userIdString = "";
            BufferedReader br = new BufferedReader(new FileReader(filename));
            String line = br.readLine();

            //get all data
            while (line != null) {
                // edge case for an empty file or line
                if (line.equals("")) {
                    line = br.readLine();
                    continue;
                }
                lines.add(line);
                line = br.readLine();
            }

            BufferedWriter bw = new BufferedWriter(new FileWriter(filename));
            for (String eachLine : lines) {
                String[] components = eachLine.split(", ");
                if (components[0].equals(userName)) {
                    flag = true;
                    userIdString = components[0];
                } else {
                    bw.write(eachLine + "\n");
                }
            }

            lines = new ArrayList<>();
            BufferedReader brPosts = new BufferedReader(new FileReader("posts.txt"));
            line = brPosts.readLine();
            while (line != null) {
                lines.add(line);
                line = brPosts.readLine();
            }
            BufferedWriter bwPosts = new BufferedWriter(new FileWriter("posts.txt"));
            for (String eachLine : lines) {
                String[] components = eachLine.split(", ");
                if (components[1].equals(userName)) {
                } else {
                    bwPosts.write(eachLine + "\n");
                }
            }

            lines = new ArrayList<>();
            BufferedReader brComments = new BufferedReader(new FileReader("comments.txt"));
            line = brComments.readLine();
            while (line != null) {
                lines.add(line);
                line = brComments.readLine();
            }
            BufferedWriter bwComments = new BufferedWriter(new FileWriter("comments.txt"));
            for (String eachLine : lines) {
                String[] components = eachLine.split(", ");
                if (components[2].equals(userName)) {
                } else {
                    bwComments.write(eachLine + "\n");
                }
            }

            br.close();
            bw.close();
            brPosts.close();
            bwPosts.close();
            brComments.close();
            bwComments.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
        return flag;

    }
}