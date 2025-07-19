// ✅ voz_reactiva_screen.dart completo y limpio y funcional

import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:provider/provider.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:string_similarity/string_similarity.dart';
import '../data/datos_efectos.dart';
import '../data/alias_nombres.dart';
import '../providers/progreso_provider.dart';
import '../controladores/escena_cache_controller.dart';
import '../generadores/ia_image_generator.dart';


class VozReactivaScreen extends StatefulWidget {
  final String titulo;
  final String contenido;

  const VozReactivaScreen({
    super.key,
    required this.titulo,
    required this.contenido,
  });

  @override
  State<VozReactivaScreen> createState() => _VozReactivaScreenState();
}

class _VozReactivaScreenState extends State<VozReactivaScreen> {
  String? libroId;
  int? capituloIndex;

  late stt.SpeechToText _speech;
  bool _listening = false;
  String _textoReconocido = '';
  double _opacidadImagen = 0;
  Timer? _reinicioPorInactividad;
  Timer? _timerOcultarEscena;
  final Map<String, DateTime> _tiempoUltimaReproduccion = {};
  List<String> _paginas = [];
  int _paginaActual = 0;
  String? _escenaActiva;
  List<Map<String, dynamic>> _elementosEscena = [];
  Map<String, dynamic> _escenas = {};
  static const Duration _delayEntreActivaciones = Duration(seconds: 4);
  final List<String> _efectosActivos = [];

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _paginas = _dividirEnPaginas(widget.contenido);
    Future.microtask(() async {
      _cargarArgumentos();
      await _cargarEscenas();
      _iniciarEscucha();
      _verificarYMostrarEscenaIA();
    });
  }
Future<void> generarImagenIADesdeScript() async {
  const rutaScript = 'C:\\PROYECTOS-FLUTTER\\lia_ia_local\\prueba_sd.py';

  try {
    final resultado = await Process.run('python', [rutaScript]);

    if (resultado.exitCode == 0) {
      debugPrint('✅ Imagen generada correctamente');
      debugPrint(resultado.stdout);
    } else {
      debugPrint('❌ Error al generar imagen');
      debugPrint(resultado.stderr);
    }
  } catch (e) {
    debugPrint('❌ Excepción al ejecutar el script: $e');
  }
}
Future<void> generarImagenConPrompt(String prompt, {int width = 1080, int height = 1920}) async {
  const rutaScript = 'C:\\PROYECTOS-FLUTTER\\lia_ia_local\\generar_sd_desde_prompt.py';

  try {
    final resultado = await Process.run('python', [rutaScript, prompt, '$width', '$height']);

    if (resultado.exitCode == 0) {
      debugPrint('✅ Imagen generada con prompt: $prompt ($width x $height)');
      debugPrint(resultado.stdout);
    } else {
      debugPrint('❌ Error generando imagen con prompt');
      debugPrint(resultado.stderr);
    }
  } catch (e) {
    debugPrint('❌ Excepción: $e');
  }
}

  void _iniciarEscucha() async {
    final disponible = await _speech.initialize(onError: (val) => print('Error: $val'));
    if (!disponible) return;

    setState(() => _listening = true);

    _speech.listen(
      onResult: (val) {
        if (val.recognizedWords.trim().isEmpty) return;
        _procesarReconocimiento(val.recognizedWords.toLowerCase());
        _reiniciarPorInactividad();
      },
      listenMode: stt.ListenMode.dictation,
      partialResults: true,
      pauseFor: const Duration(seconds: 60),
    );
  }

  void _toggleEscucha() {
    _listening ? _speech.stop() : _iniciarEscucha();
    setState(() => _listening = !_listening);
  }

  void _reiniciarPorInactividad() {
    _reinicioPorInactividad?.cancel();
    _reinicioPorInactividad = Timer(const Duration(seconds: 4), () {
      if (mounted && _listening) {
        _speech.stop();
        Future.delayed(const Duration(milliseconds: 300), () {
          if (mounted) _iniciarEscucha();
        });
      }
    });
  }

  void _cargarArgumentos() {
    final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    libroId = args?['libroId'];
    capituloIndex = args?['capituloIndex'];
  }

  Future<void> _cargarEscenas() async {
    final texto = await rootBundle.loadString('lib/data/escenas.json');
    final json = jsonDecode(texto);
    setState(() => _escenas = Map<String, dynamic>.from(json));
  }

  List<String> _dividirEnPaginas(String texto) {
    final palabras = texto.split(RegExp(r'\s+'));
    const palabrasPorPagina = 300;
    final paginas = <String>[];
    for (int i = 0; i < palabras.length; i += palabrasPorPagina) {
      final pagina = palabras.skip(i).take(palabrasPorPagina).join(' ');
      paginas.add(pagina.trim());
    }
    return paginas;
  }

  bool coincide(String texto, String clave, List<String>? alias) {
    if (texto.contains(clave)) return true;
    if (alias != null && alias.any((a) => texto.contains(a))) return true;
    for (final palabra in texto.split(' ')) {
      if (palabra.similarityTo(clave) > 0.75) return true;
      if (alias != null && alias.any((a) => palabra.similarityTo(a) > 0.75)) return true;
    }
    return false;
  }

  bool _puedeActivar(String palabra) {
    final ahora = DateTime.now();
    final ultimo = _tiempoUltimaReproduccion[palabra];
    if (ultimo == null || ahora.difference(ultimo) > _delayEntreActivaciones) {
      _tiempoUltimaReproduccion[palabra] = ahora;
      return true;
    }
    return false;
  }

  void _procesarReconocimiento(String texto) {
    setState(() {
      _textoReconocido = texto;
      final clavesOrdenadas = efectos.keys.toList()..sort((a, b) => b.length.compareTo(a.length));
      final detectadas = <String>{};

      for (final palabra in clavesOrdenadas) {
        final alias = aliasNombres[palabra];
        if (coincide(texto, palabra, alias) && !detectadas.contains(palabra) && _puedeActivar(palabra)) {
          detectadas.add(palabra);
          _activarEfecto(palabra);
          _activarEscenaDesdeJson(palabra);
        }
      }

      _escenas.forEach((clave, escena) {
        if (detectadas.contains(clave)) return;
        final palabrasClave = List<String>.from(escena['palabras_clave'] ?? []);
        for (final frase in palabrasClave) {
          if (texto.contains(frase.toLowerCase()) && _puedeActivar(clave)) {
            _activarEscenaDesdeJson(clave);
            break;
          }
        }
      });
    });
  }

  void _activarEfecto(String palabra) async {
    final archivo = efectos[palabra];
    if (archivo == null) return;

    final player = AudioPlayer();
    _efectosActivos.add(archivo);
    setState(() => _opacidadImagen = 1);

    try {
      await player.setSource(AssetSource('sounds/$archivo.mp3'));
      await player.resume();
    } catch (e) {
      print('Error al reproducir $archivo: $e');
    }

    Future.delayed(const Duration(seconds: 5), () async {
      if (!mounted) return;
      await player.stop();
      setState(() {
        _efectosActivos.remove(archivo);
        if (_efectosActivos.isEmpty) _opacidadImagen = 0;
      });
    });
  }

  void _activarEscenaDesdeJson(String clave) {
    final escena = _escenas[clave];
    if (escena == null) return;

    setState(() {
      _escenaActiva = clave;
      _elementosEscena = List<Map<String, dynamic>>.from(escena['elementos'] ?? []);
    });

    final sonido = escena['sonido_ambiente'];
    if (sonido != null) {
      final player = AudioPlayer();
      player.setSource(AssetSource(sonido)).then((_) => player.resume());
      Future.delayed(const Duration(seconds: 7), () => player.stop());
    }

    _timerOcultarEscena?.cancel();
    _timerOcultarEscena = Timer(const Duration(seconds: 7), () {
      setState(() {
        _escenaActiva = null;
        _elementosEscena.clear();
      });
    });
  }

  void _mostrarDialogoPruebaTexto() {
    showDialog(
      context: context,
      builder: (ctx) {
        final controller = TextEditingController();
        return AlertDialog(
          title: const Text('Prueba sin voz'),
          content: TextField(
            controller: controller,
            decoration: const InputDecoration(labelText: 'Ingresa texto'),
          ),
          actions: [
            TextButton(
              child: const Text('Cancelar'),
              onPressed: () => Navigator.of(ctx).pop(),
            ),
            ElevatedButton(
              child: const Text('Activar'),
              onPressed: () {
                Navigator.of(ctx).pop();
                _procesarReconocimiento(controller.text.toLowerCase());
              },
            ),
          ],
        );
      },
    );
  }

  void _probarImagenIA() async {
    final imagenGenerada = await IAImageGenerator.generarImagenDesdePrompt(
      'A glowing ancient forest with floating lights',
      'escena_bosque',
    );

    if (imagenGenerada != null && mounted) {
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text('Imagen generada por IA'),
          content: Image.file(imagenGenerada),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cerrar'),
            ),
          ],
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No se pudo generar la imagen')),
      );
    }
  }

  Future<void> _verificarYMostrarEscenaIA() async {
    final idLibro = libroId ?? 'demo';
    final cap = capituloIndex ?? 0;
    final escenaId = _paginaActual + 1;

    final imagen = await EscenaCacheController.cargarImagenEscena(
      libroId: idLibro,
      capitulo: cap,
      escenaId: escenaId,
    );

    if (imagen != null && mounted) {
      setState(() {
        _elementosEscena = [
          {'src': imagen.path}
        ];
      });

      _timerOcultarEscena?.cancel();
      _timerOcultarEscena = Timer(const Duration(seconds: 10), () {
        if (!mounted) return;
        setState(() {
          _escenaActiva = null;
          _elementosEscena.clear();
        });
      });
    }
  }

  void _generarEscenasCapitulo1() async {
    final escenas = [
      {'id': 1, 'prompt': 'A warm family home in the suburbs...'},
      {'id': 2, 'prompt': 'A boy sitting on a cardboard box...'},
      {'id': 3, 'prompt': 'A small family arriving at a house...'},
      {'id': 4, 'prompt': 'A kind mother talking to her son...'},
      {'id': 5, 'prompt': 'A teenage boy standing nervously...'},
    ];

    final idLibro = libroId ?? 'angelo_proyecto_ditox';
    final cap = capituloIndex ?? 0;

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('⏳ Generando escenas IA...')),
    );

    for (final escena in escenas) {
      final id = escena['id'] as int;
      final prompt = escena['prompt'] as String;

      final imagen = await IAImageGenerator.generarImagenDesdePrompt(prompt, 'escena_cap1_$id');
      if (imagen != null) {
        final guardada = await EscenaCacheController.guardarImagenEscena(
          libroId: idLibro,
          capitulo: cap,
          escenaId: id,
          imagen: imagen,
        );
        print('✅ Escena $id guardada en: ${guardada.path}');
      } else {
        print('❌ No se pudo generar la escena $id');
      }
    }

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('✅ Escenas IA generadas')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text(widget.titulo),
        backgroundColor: Colors.cyan[900],
      ),
      body: Stack(
        children: [
          if (_elementosEscena.isNotEmpty)
            Positioned.fill(
              child: Stack(
                children: _elementosEscena.map((elemento) {
                  final src = elemento['src'];
                  return AnimatedOpacity(
                    opacity: 1,
                    duration: const Duration(milliseconds: 500),
                    child: src.toString().endsWith('.json')
                        ? Lottie.network(src, fit: BoxFit.cover)
                        : Image.asset(src, fit: BoxFit.cover),
                  );
                }).toList(),
              ),
            ),
          if (_efectosActivos.isNotEmpty)
            Positioned.fill(
              child: AnimatedOpacity(
                opacity: _opacidadImagen,
                duration: const Duration(milliseconds: 300),
                child: Stack(
                  children: _efectosActivos.map((archivo) {
                    return Positioned.fill(
                      child: Image.asset(
                        'assets/animaciones/$archivo.png',
                        fit: BoxFit.cover,
                      ),
                    );
                  }).toList(),
                ),
              ),
            ),
          Column(
            children: [
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Text(
                    _paginas[_paginaActual],
                    style: const TextStyle(
                      fontSize: 20,
                      color: Colors.white,
                      height: 1.5,
                    ),
                    textAlign: TextAlign.justify,
                  ),
                ),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  IconButton(
                    icon: const Icon(Icons.chevron_left, size: 32),
                    onPressed: _paginaActual > 0
                        ? () {
                            setState(() => _paginaActual--);
                            _verificarYMostrarEscenaIA();
                          }
                        : null,
                    color: Colors.white,
                  ),
                  Text(
                    'Página ${_paginaActual + 1}/${_paginas.length}',
                    style: const TextStyle(color: Colors.white),
                  ),
                  IconButton(
                    icon: const Icon(Icons.chevron_right, size: 32),
                    onPressed: _paginaActual < _paginas.length - 1
                        ? () {
                            setState(() => _paginaActual++);
                            _verificarYMostrarEscenaIA();
                          }
                        : null,
                    color: Colors.white,
                  ),
                ],
              ),
              Container(
                color: Colors.grey[900],
                padding: EdgeInsets.fromLTRB(16, 12, 16, MediaQuery.of(context).padding.bottom + 20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    ElevatedButton.icon(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(Icons.arrow_back),
                      label: const Text('Modo clásico'),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.blueGrey),
                    ),
                    ElevatedButton.icon(
                      onPressed: _toggleEscucha,
                      icon: Icon(_listening ? Icons.mic_off : Icons.mic),
                      label: Text(_listening ? 'Detener voz' : 'Activar voz'),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.cyan[700]),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),

            floatingActionButton: Column(
  mainAxisSize: MainAxisSize.min,
  children: [
    FloatingActionButton(
      heroTag: 'btn1',
      onPressed: _mostrarDialogoPruebaTexto,
      backgroundColor: Colors.deepPurple,
      child: const Icon(Icons.bug_report),
      tooltip: 'Probar escena o efecto',
    ),
    const SizedBox(height: 12),
    FloatingActionButton(
      heroTag: 'btn2',
      onPressed: _probarImagenIA,
      backgroundColor: Colors.green,
      child: const Icon(Icons.image),
      tooltip: 'Generar imagen IA (API)',
    ),
    const SizedBox(height: 12),
    FloatingActionButton(
      heroTag: 'btn3',
      onPressed: _generarEscenasCapitulo1,
      backgroundColor: Colors.orange,
      child: const Icon(Icons.auto_fix_high),
      tooltip: 'Generar escenas Capítulo 1 (API)',
    ),
    const SizedBox(height: 12),
    FloatingActionButton(
      heroTag: 'btn4',
      onPressed: generarImagenIADesdeScript,
      backgroundColor: Colors.teal,
      child: const Icon(Icons.flash_on),
      tooltip: 'Generar imagen local (GPU - script prueba)',
    ),
    const SizedBox(height: 12),
    FloatingActionButton(
      heroTag: 'btn5',
      onPressed: () {
        generarImagenConPrompt(
          "ciudad futurista en ruinas iluminada con neón y cielo oscuro",
          width: 768,
          height: 1024,
        );
      },
      backgroundColor: Colors.indigo,
      child: const Icon(Icons.build_circle),
      tooltip: 'Imagen local con resolución custom',
          ),
        ],
      ),
    );
  }
}

