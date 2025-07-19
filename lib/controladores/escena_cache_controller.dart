import 'dart:io';
import 'package:path_provider/path_provider.dart';

class EscenaCacheController {
  static Future<String> _basePath() async {
    final dir = await getApplicationDocumentsDirectory();
    return '${dir.path}/cache_escenas';
  }

  static Future<File> guardarImagenEscena({
    required String libroId,
    required int capitulo,
    required int escenaId,
    required File imagen,
  }) async {
    final base = await _basePath();
    final dir = Directory('$base/$libroId/cap_$capitulo');
    if (!await dir.exists()) await dir.create(recursive: true);

    final destino = File('${dir.path}/escena_$escenaId.jpg');
    return await imagen.copy(destino.path);
  }

  static Future<File?> cargarImagenEscena({
    required String libroId,
    required int capitulo,
    required int escenaId,
  }) async {
    final base = await _basePath();
    final imagen = File('$base/$libroId/cap_$capitulo/escena_$escenaId.jpg');
    return await imagen.exists() ? imagen : null;
  }
}
