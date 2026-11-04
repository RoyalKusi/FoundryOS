import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

abstract class AppTypography {
  static TextStyle largeTitle(BuildContext context) => GoogleFonts.inter(fontSize: 34, height: 41 / 34, fontWeight: FontWeight.w700, letterSpacing: 0.37);
  static TextStyle title1(BuildContext context) => GoogleFonts.inter(fontSize: 28, height: 34 / 28, fontWeight: FontWeight.w700, letterSpacing: 0.36);
  static TextStyle title2(BuildContext context) => GoogleFonts.inter(fontSize: 22, height: 28 / 22, fontWeight: FontWeight.w600, letterSpacing: 0.35);
  static TextStyle headline(BuildContext context) => GoogleFonts.inter(fontSize: 17, height: 22 / 17, fontWeight: FontWeight.w600, letterSpacing: -0.41);
  static TextStyle body(BuildContext context) => GoogleFonts.inter(fontSize: 17, height: 22 / 17, fontWeight: FontWeight.w400, letterSpacing: -0.41);
  static TextStyle footnote(BuildContext context) => GoogleFonts.inter(fontSize: 13, height: 18 / 13, fontWeight: FontWeight.w400, letterSpacing: -0.08);
}
