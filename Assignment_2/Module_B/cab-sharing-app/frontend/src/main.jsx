import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { Box, ChakraProvider, extendTheme, ColorModeScript } from '@chakra-ui/react';
import { BrowserRouter } from 'react-router-dom';

const theme = extendTheme({
  config: {
    initialColorMode: 'dark',
    useSystemColorMode: false,
  },
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      {/* <Box bg="red.500" minH="100vh"> */}
        <BrowserRouter>
          <App />
        </BrowserRouter>
      {/* </Box> */}
    </ChakraProvider>
  </StrictMode>
);