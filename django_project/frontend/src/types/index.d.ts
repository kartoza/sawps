import {
    PaletteColorOptions
  } from '@mui/material/styles';

declare module '@mui/material/styles' {
    interface CustomPalette {
        primary: PaletteColorOptions;
    }
    interface Palette extends CustomPalette {}
    interface PaletteOptions extends CustomPalette {}
  }
  
  declare module '@mui/material/Button' {
    interface ButtonPropsColorOverrides {
        primary: true;
    }
  }