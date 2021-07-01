package Models;

import Controllers.Utility;
public class User {
    private final String username;
    private String password;
    private final String createdOn;
    private final String plateNumber;


    public User(String username, String password, String plateNumber) {
        this.username = username;
        this.password = password;
        this.plateNumber = plateNumber;
        this.createdOn = Utility.getCurrentTime();
    }

    public User(String username, String password, String createdOn, String plateNumber) {
        this.username = username;
        this.password = password;
        this.createdOn = createdOn;
        this.plateNumber = plateNumber;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getPlateNumber() { return plateNumber;}

    public String getCreatedOn() {
        return createdOn;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return String.format("%s, %s, %s,  %s", username, password, plateNumber,  createdOn);
    }
}