<?php
require_once 'db.php';

if (isset($_POST['submit'])) {
    $student_id = $_POST['student_id'];
    $student_name = $_POST['student_name'];
    $report_date = $_POST['report_date'];

    // Handle the image file upload
    if (isset($_FILES['profile_picture']) && $_FILES['profile_picture']['error'] == 0) {
        $image = $_FILES['profile_picture']['tmp_name'];
        $imgContent = file_get_contents($image); // Convert image to binary string
    } else {
        die("Error uploading profile picture.");
    }

    // Use prepared statements to prevent SQL Injection
    $stmt = $conn->prepare("INSERT INTO Student (student_ID, student_name, report_date, profile_picture) VALUES (?, ?, ?, ?)");
    
    // "ssss" means 4 strings (binary data is sent via send_long_data or treated as string in packet)
    $stmt->bind_param("ssss", $student_id, $student_name, $report_date, $imgContent);

    if ($stmt->execute()) {
        echo "Student registered successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
}
?>
