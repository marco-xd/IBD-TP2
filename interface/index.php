<!DOCTYPE html>
<html lang="pt_br">
	<head>
		<meta charset="utf-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />

		<title>TP IBD</title>

		<link href="css/bootstrap.min.css" rel="stylesheet" />
		<link href="css/style.css" rel="stylesheet" />
		<!--[if lt IE 9]>
			<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
			<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script src="js/bootstrap.min.js"></script>
		
		<script type="text/javascript">
			$(document).ready(function () {
				var txtbox = document.getElementById('text'),
				    ddown = document.getElementById('dropdownlist');

				ddown.value = ddown.children[0].value;
				txtbox.innerHTML = '';

				$(document.getElementById('dropdownlist')).on('change', function () {
					txtbox.innerHTML = this.value;
				});
			});
		</script>
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
				</div>
			</div>
		</nav>

		<div class="container">
				<div class="starter-template">
					<form action="query.php" method="post">
						<h3>Digite sua query:</h3>
						<textarea id="text" name="stmt"></textarea>
						<br />
						<br />
						<input type="submit" value="Enviar" />
					</form>
				</div>
		</div>


		<div class="form-group">
			<select class="form-control" id="dropdownlist">
				<option value="" selected>SELECIONE SUA PESQUISA</option>

				<option value="SELECT `countryformalname`, SUM(`price`) FROM `countries` NATURAL JOIN `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `is_free` = 0 GROUP BY `countryformalname` ORDER BY SUM(`price`);">
					Mostrar o nome do pa&iacute;s seguido de o total gasto (centavos) por jogos não gr&aacute;tis
				</option>

				<option value="SELECT `appid` FROM `details` WHERE `linux_support` = 1 AND `appid` NOT IN (SELECT DISTINCT `appid` FROM `news`);">
					Mostrar os appid dos jogos que possuem suporte para linux e n&atilde;o possuem alguma not&iacute;cia
				</option>
				
				<option value="SELECT `appid` FROM `details` WHERE `linux_support` = 1 AND `mac_support` = 1 AND `windows_support` = 1 ORDER BY `appid`;">
					Mostrar o appid dos jogos que possuem suporte para todas as plataformas (linux, mac e windows)
				</option>
				
				<option value="SELECT `avatarmedium`, `steamid`, `personaname`, MAX(`playtime_forever`), `appid` FROM `summaries` NATURAL JOIN `owned` GROUP BY `steamid`">
					Mostrar o id, nome e avatar de cada jogador e o id do jogo que ele mais jogou
				</option>
				
				<option value="SELECT `appid`, `header_image`, COUNT(`steamid`), SUM(`playtime_forever`) FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` GROUP BY `appid`;">
					Mostrar o id, a imagem, o total de players e o total de tempo jogado de cada jogo
				</option>
				
				<option value="SELECT c1.`countryformalname`, aux.id, aux.nome, aux.avatarfull, MAX(aux.total) FROM (SELECT s.`steamid` AS id, s.`personaname` AS NOME, s.`loccountrycode` AS loccountrycode, COUNT(pa.`achieved`) AS total, s.`avatarfull` as avatarfull FROM `summaries` s NATURAL JOIN `playerachievements` pa GROUP BY s.`steamid`) aux NATURAL JOIN `countries` c1 GROUP BY c1.`countryformalname` ORDER BY MAX(total);">
					Mostrar nome do pa&iacute;s e nome e avatar do habitante que mais possui conquistas
				</option>
				
				<option value="SELECT D.`appid`, D.`dev_name` FROM `developers` D JOIN `publishers` P ON D.`appid` = P.`appid` AND D.`dev_name` = P.`pub_name` ORDER BY D.`appid`;">
					Selecionar os jogos que possuem desenvolvedores e divulgadores iguais
				</option>
				
				<option value="SELECT `steamid1`, `steamid2`, a.`appid` FROM `friends`, `owned` a, `owned` b WHERE a.`steamid` = `steamid1` AND b.`steamid` = `steamid2` AND a.`appid` = b.`appid` ORDER BY `steamid1`;">
					Selecionar todos os amigos que possuem jogos em comum e mostrar o id do jogo
				</option>
				
				<option value="SELECT `steamid`, `personaname`, CASE WHEN SUM(`price`) > 10000 THEN &quot;verdadeiro&quot; ELSE &quot;falso&quot; END AS verdadeiro_ou_falso FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `is_free` = 0 GROUP BY `steamid`;">
					Mostrar &quot;verdadeiro&quot; se uma pessoa gastou mais que R$ 100,00 em jogos e &quot;falso&quot; caso contr&aacute;rio
				</option>
				
				<option value="SELECT `steamid`, `personaname`, `header_image` FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `playtime_2weeks` > 0 AND `supported_languages` LIKE '%Portuguese%';">
					Se a pessoa jogou um jogo com suporte para l&iacute;ngua portuguesa nas &uacute;timas duas semanas, exibir steamid e nome da pessoa e imagem do jogo
				</option>
				
				<option value="SELECT `countryformalname`, CONCAT(ROUND((`totalbuyers` / `totalplayers`) * 100), '%') AS percentage FROM (SELECT `loccountrycode`, `countryformalname`, COUNT(DISTINCT `steamid`) AS totalbuyers FROM `summaries` NATURAL JOIN `countries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `price` > 0 AND `is_free` = 0 AND `countryformalname` != '' GROUP BY `loccountrycode`) b NATURAL JOIN (SELECT `loccountrycode`, COUNT(DISTINCT `steamid`) AS totalplayers FROM `summaries` NATURAL JOIN `countries` GROUP BY `loccountrycode`) p GROUP BY `countryformalname`;">
					Para cada pa&iacute;s que tem jogadores que compram jogos, mostrar a porcentagem dos que possuem ao menos um jogo comprado
				</option>
				
				<option value="SELECT c.`countryformalname`, CONCAT('R$ ', ROUND(AVG(aux.totalpessoa) / 100, 2)) as money FROM `countries` c NATURAL JOIN (SELECT s.`loccountrycode`, SUM(d.`price`) AS totalpessoa FROM `summaries` s NATURAL JOIN `owned` o NATURAL JOIN `details` d WHERE d.`price` > 0 GROUP BY s.`steamid`) aux WHERE c.`countryformalname` != '' GROUP BY c.`countryformalname` ORDER BY c.`countryformalname`;">
					Mostrar a m&eacute;dia de dinheiro gasto por pessoa por cada pa&iacute;s
				</option>
				
				<option value="SELECT `personaname`, `appid` FROM `summaries` NATURAL JOIN `owned` NATURAL JOIN `details` WHERE `playtime_forever` = 0 AND `price` > 0;">
					Selecionar o nome das pessoas e seus jogos comprados que n&atilde;o foram jogados
				</option>
			</select>
		</div>

	</body>
</html>
