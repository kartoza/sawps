import { createTheme } from '@mui/material/styles';

export const uniqueColors = [
  'rgba(112, 178, 118, 1)',
  'rgba(250, 167, 85, 1)',
  'rgba(157, 133, 190, 1)',
  '#FF5252',
  '#616161',
  // additional transparency colors for years
  'rgba(112, 178, 118, 0.5)', // 50% transparency
  'rgba(255, 82, 82, 0.5)', // 50% transparency
  'rgba(97, 97, 97, 0.5)', // 50% transparency
  'rgba(157, 133, 190, 0.5)', // 50% transparency
  'rgba(250, 167, 85, 0.5)', // 50% transparency
];

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
    fontFamily: '"Inter", sans-serif',
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
