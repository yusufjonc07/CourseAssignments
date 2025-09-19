<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Students Database</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  
<h1>Students personal information</h1>

<?php
$servername = "localhost";
$username = "root";
$password = "root";
$databasename = "school";

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
$query = "SELECT * FROM `student`;";

$columns = [
  'first_name' => 'First name',
  'last_name' => 'Last name',
  'age' => 'Age',
  'gender' => 'Gender',
  'address' => 'Address',
  'university_name' => 'University name',
  'semester' => 'Semester #',
  'gpa' => 'GPA',
  'nationality' => 'Nationality',
  'hobby' => 'Hobby'
];

// FETCHING DATA FROM DATABASE 
$result = $conn->query($query);

if ($result->num_rows > 0) { ?>

<div class="table-container">
  <?php while ($row = $result->fetch_assoc()) {
    ?>
    <table border="1">
      <thead>
        <tr>
          <th>Sr.#</th>
          <th>Attribute</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <?php $sr = 0;
        foreach ($columns as $key => $value) { ?>
          <tr>
            <td><?= ++$sr; ?></td>
            <td><?= $value ?></td>
            <td><?= $row[$key] ?></td>
          </tr>
        <?php } ?>
      </tbody>
    </table>
  <?php } ?> 
  </div>  
  <?php
} else {
  echo "0 results";
}

$conn->close();

?>

</body>
</html>

