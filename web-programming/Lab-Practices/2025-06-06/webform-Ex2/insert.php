<?php
if(isset($_POST["submit"])){
include 'dbconfig.php';

$sql = "INSERT INTO entries (name, email, city, gender)
VALUES ('".$_POST["name"]."','".$_POST["email"]."','".$_POST["city"]."','".$_POST["gender"]."')";

if ($conn->query($sql) === TRUE) {
echo "
    <script type= 'text/javascript'>
        alert('New record created successfully');
    </script>";
} 
else 
{
    echo 
    "<script type= 'text/javascript'>
        alert('Error: " . $sql . "<br>" . $conn->error."');
    </script>";
}

$conn->close();
}
?>