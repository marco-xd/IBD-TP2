<!DOCTYPE html>

<html lang="pt_br">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>TP IBD</title>

    <!-- CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>

<nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a id="nomeProjeto" class="navbar-brand" href="#">TP Banco de Dados</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="index.php">Home</a></li>
            <li class="active"><a href="grupo.html">Grupo</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

<?php
$servername="localhost";
$username="hugo";
$password="";
$dbname = "imdb_top250";


//Create connection
$conn=new mysqli($servername,$username,$password,$dbname);

//Check connection
if ($conn->connect_errno) {
	die("Connection failed: " . $conn->connect_error);
}

$stmt = $_POST["stmt"];

if($result = $conn->query($stmt)){
//Imprime Tabela de Resultados

//Matriz com os dados das colunas //http://php.net/manual/pt_BR/mysqli-result.fetch-fields.php
$colunas = $result->fetch_fields();


//Imprimindo a tabela
?>

<div class="table-responsive" id="resQuery">
	<table class="table table-striped table-bordered">
		<thead>
<?php
	//Nomes das colunas
	echo "<tr>";
	foreach ($colunas as $val) {
		echo "<td>";
		printf("%s  ",$val->name);
   		echo "</td>";
	}
	echo  "</tr>";
	echo "</thead>";
	echo "<tbody>";
//Todas as linhas da query  //http://php.net/manual/pt_BR/mysqli-result.fetch-assoc.php
while( $linhas = $result->fetch_assoc() ) {
    echo "<tr>";
      foreach($linhas AS $col){
        echo "<td>";
            echo $col;
       echo "</td>";
      }
    echo  "</tr>"; 
}
	echo "</tbody>";
echo "</table>";
echo "</div>";
}
else{
	printf("Erro: %s <br>",$conn->error);
}


$result->close();
$conn->close();
?>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>


 </body>
 </html>
