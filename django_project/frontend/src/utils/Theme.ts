import { createTheme } from '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Palette {
    customColors?: PaletteCustomColors;
  }

  interface PaletteOptions {
    customColors?: PaletteCustomColorsOptions;
  }

  interface PaletteCustomColors {
    green: string;
    orange: string;
    purple: string;
  }

  interface PaletteCustomColorsOptions {
    green: string;
    orange: string;
    purple: string;
  }
}
const { palette } = createTheme();
const { augmentColor } = palette;
const createColor = (mainColor: any) => augmentColor({
  color: {
    main: mainColor,
    contrastText: '#fff'
  }
});

const theme = createTheme({
  typography: {
    fontFamily: '"Poppins", sans-serif',
  },
  palette: {
    mode: 'light',
    primary: createColor('#70B276'),
    customColors: {
      green: 'var(--green)',
      orange: 'var(--orange)',
      purple: 'var(--purple)'
    },
  },
});

export default theme;
