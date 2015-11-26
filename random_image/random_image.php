<?php

$lastmod = filemtime(__FILE__);

if (isset($_GET['s']) && isset($_GET['sid'])) {

	$steamwid = 500;
	$steamhei = 500;

	$med = ($steamwid + $steamhei) >> 1;

	putenv('GDFONTPATH=' . realpath('.'));
	$fontname = 'Chewy.ttf';
	$fontsize = $med / 12;

	$realwid = $steamwid;
	$realhei = $steamhei;

	switch ($_GET['s']) {
		case 'small': $realwid = 32; $realhei = 32; break;
		case 'medium': $realwid = 64; $realhei = 64; break;
		default: $realwid = 184; $realhei = 184; break;
	}

	$steamid = intval($_GET['sid']);

	$etag = md5($realwid . 'x' . $realhei . '-' . $steamid);

	if ((!isset($_SERVER['HTTP_IF_MODIFIED_SINCE']) || strtotime($_SERVER['HTTP_IF_MODIFIED_SINCE']) !== $lastmod)
	&& (!isset($_SERVER['HTTP_IF_NONE_MATCH']) || $_SERVER['HTTP_IF_NONE_MATCH'] !== $etag)) {

		mt_srand($steamid);

		$img = imagecreatetruecolor($steamwid, $steamhei);

		imagesetthickness ($img, 1);

		$red = mt_rand(150, 255);
		$green = mt_rand(150, 255);
		$blue = mt_rand(150, 255);
		$bg = imagecolorallocate($img, $red, $green, $blue);
		imageantialias($img, true);
		imagefilledrectangle($img, 0, 0, $steamwid - 1, $steamhei - 1, $bg);

		$balls = mt_rand(150, 200);

		for ($i = 0; $i < $balls; $i++) {

			$red = mt_rand(0, 255);
			$green = mt_rand(0, 255);
			$blue = mt_rand(0, 255);
			$alpha = mt_rand(50, 127);
			$color = imagecolorallocatealpha($img, $red, $green, $blue, $alpha);

			$radius = mt_rand($med >> 3, $med >> 1);
			$x = mt_rand(0, $steamwid);
			$y = mt_rand(0, $steamhei);

			imagefilledellipse($img, $x, $y, $radius, $radius, $color);
		}

		$black = imagecolorallocate($img, 0, 0, 0);
		imagerectangle($img, 0, 0, $steamwid - 1, $steamhei - 1, $black);

		$fontangle = mt_rand(-30, 30);

		$fontbbox = imagettfbbox($fontsize, $fontangle, $fontname, $steamid);
		$txtwid = $fontbbox[2] - $fontbbox[0];
		$txthei = $fontbbox[3] - $fontbbox[1];
		imagettftext($img, $fontsize, $fontangle, ($steamwid - $txtwid) >> 1, ($steamhei - $txthei) >> 1, $black, $fontname, $steamid);

		$rsz = imagecreatetruecolor($realwid, $realhei);
		imagecopyresampled($rsz, $img, 0, 0, 0, 0, $realwid, $realhei, $steamwid, $steamhei);

		imagedestroy($img);

		header('Content-Type: image/png');
		header('Cache-Control: public');
		header('Pragma: cache');
		header('Last-Modified: ' . gmdate('D, d M Y H:i:s ', $lastmod) . 'GMT');
		header('ETag: ' . $etag);

		imagepng($rsz);
		imagedestroy($rsz);

	} else {

		header('HTTP/1.1 304 Not Modified');

	}

	exit;
}

?>