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
            <li class="active"><a href="er.html">Esquema ER</a></li>
            <li class="active"><a href="relacional.html">Esquema Relacional</a></li>
            <li class="active"><a href="grupo.html">Grupo</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
      	<div class="starter-template">
		    <form action="query.php" method="post">
			<h3>Digite sua query:</h3> <textarea id="text" name="stmt" rows="10" cols="70"> </textarea><br><br>
			<input type="submit">
			</form>
      	</div>
    </div><!-- /.container -->


    <div class="form-group">
      <select class="form-control" id="dropdownlist">
        <option value=""> SELECIONE SUA PESQUISA</option>
        <option value="SELECT movie_name FROM movie M, role R, role_type T, person P WHERE M.movie_id = R.movie_id AND R.person_id = P.person_id AND R.role_type_id = T.role_type_id AND person_name = &quotSpielberg, Steven&quot AND type_name = &quotdirector&quot ;">
                        Selecionar todos os filmes nos quais Steven Spielberg foi diretor</option>
        <option value="SELECT  person_id as id, person_name as name, movie_name as movie FROM movie NATURAL JOIN role NATURAL JOIN person WHERE person_name=&quotMcKellen, Ian&quot ;">
                        Selecionar o id, nome e nome do filme que Ian Mckellen participou</option>
        <option value="text3">text3</option>rnatively, you can delimit the attribute value with single quotes:
        <option value="text4">text4</option>
      </select>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
    
    <script type="text/javascript">
      var mytextbox = document.getElementById('text');
      var mydropdown = document.getElementById('dropdownlist');

      mydropdown.onchange = function(){
           //mytextbox.value = mytextbox.value  + this.value; //to appened
           mytextbox.innerHTML = this.value;
      }
    </script>

  </body>
</html>
