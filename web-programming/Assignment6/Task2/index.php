<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Famous Sports</title>
  <link rel="stylesheet" href="../../Assignment3/bootstrap.min.css">
</head>
<body class="p-3">
  
<h1>Sports with rating over 50</h1>

<?php
$servername = "localhost";
$username = "root";
$password = "root";
$databasename = "famous-sports";

// CREATE CONNECTION 
$conn = new mysqli(
  $servername,
  $username,
  $password,
  $databasename
);

// GET CONNECTION ERRORS 
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

// SQL QUERY 
$query = "SELECT * FROM `sports` WHERE rating > 50;";

// FETCHING DATA FROM DATABASE 
$result = $conn->query($query);

if ($result->num_rows > 0) { ?>


    <table class="table table-sm table-bordered table-striped w-25">
      <thead>
        <tr>
          <th>Sports Name</th>
          <th>Rating</th>
        </tr>
      </thead>
      <tbody>
        <?php while ($row = $result->fetch_assoc()) { ?>
          <tr>
            <td><?= $row['sports_name'] ?></td>
            <td><?= $row['rating'] ?></td>
          </tr>
        <?php } ?>
      </tbody>
    </table>
  <?php
} else {
  echo "0 results";
}
$conn->close();
?>
</body>
</html>

