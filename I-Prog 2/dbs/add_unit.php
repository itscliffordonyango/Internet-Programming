<?php
require_once 'db.php';

if (isset($_POST['submit'])) {
    $unit_name = $_POST['unit_name'];

    // Use prepared statements for security
    $stmt = $conn->prepare("INSERT INTO Unit (unit_name) VALUES (?)");
    $stmt->bind_param("s", $unit_name);

    if ($stmt->execute()) {
        echo "Unit '" . htmlspecialchars($unit_name) . "' added successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
}
?>
