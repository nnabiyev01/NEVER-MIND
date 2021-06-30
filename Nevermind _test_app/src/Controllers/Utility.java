package Controllers;
import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;


public class Utility {
    public static String getCurrentTime() {
        TimeZone.setDefault(TimeZone.getTimeZone("UTC"));
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        LocalDateTime now = LocalDateTime.now();
        return dtf.format(now);
    }

    public static int getId(String filename) {
        int currentLastId =  0;
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String lastLine = "";
            String line;
            while ((line = br.readLine()) != null) {
                lastLine = line;
            }
            if (lastLine.equals(""))
                currentLastId = 1;
            else {
                currentLastId = Integer.parseInt(lastLine.split(",")[0]);
                currentLastId += 1;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return currentLastId;
    }


}