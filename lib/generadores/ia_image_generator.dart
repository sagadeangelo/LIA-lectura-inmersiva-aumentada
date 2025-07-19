import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';

class IAImageGenerator {
  static const String _apiKey = 'r8_8lF1EiBP3BRt5TaluWqm0dd6Z66OOuW21pHeI'; // 🔐 Reemplaza esto
  static const String _endpoint =
      'https://api.replicate.com/v1/predictions';

  static Future<File?> generarImagenDesdePrompt(String prompt, String nombreArchivo) async {
    try {
      final response = await http.post(
        Uri.parse(_endpoint),
        headers: {
          'Authorization': 'Token $_apiKey',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          "version": "ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4", // ✅ versión actual y válida
          "input": {
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "num_outputs": 1
          }
        }),
      );

      final Map<String, dynamic> decoded = jsonDecode(response.body);

      if (response.statusCode != 201 || decoded['id'] == null) {
        print('Error al iniciar generación: ${response.body}');
        return null;
      }

      final String predictionId = decoded['id'];

      // Esperar a que se complete
      while (true) {
        final poll = await http.get(
          Uri.parse("$_endpoint/$predictionId"),
          headers: {'Authorization': 'Token $_apiKey'},
        );
        final resultado = jsonDecode(poll.body);
        if (resultado['status'] == 'succeeded') {
          final url = resultado['output'][0];
          return await _descargarImagen(url, nombreArchivo);
        } else if (resultado['status'] == 'failed') {
          print('La generación falló');
          return null;
        }
        await Future.delayed(const Duration(seconds: 2));
      }
    } catch (e) {
      print('Error generando imagen IA: $e');
      return null;
    }
  }

  static Future<File> _descargarImagen(String url, String nombreArchivo) async {
    final response = await http.get(Uri.parse(url));
    final dir = await getApplicationDocumentsDirectory();
    final file = File('${dir.path}/$nombreArchivo.jpg');
    await file.writeAsBytes(response.bodyBytes);
    return file;
  }
}
