package Models;

import Controllers.Utility;

public class User {
    private final String username;
    private String password;
    private final String createdOn;

    public User(String username, String password) {
        this.username = username;
        this.password = password;
        this.createdOn = Utility.getCurrentTime();
    }

    public User(String username, String password, String createdOn) {
        this.username = username;
        this.password = password;
        this.createdOn = createdOn;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getCreatedOn() {
        return createdOn;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return String.format("%s, %s, %s", username, password, createdOn);
    }
}