import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { Box, ChakraProvider, extendTheme, ColorModeScript } from '@chakra-ui/react';
import { BrowserRouter } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';

const theme = extendTheme({
  config: {
    initialColorMode: 'dark',
    useSystemColorMode: false,
  },
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <GoogleOAuthProvider clientId="1096112354551-ngdlkcddrsgbdtreja9q0j9vdld4j3e7.apps.googleusercontent.com">
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      {/* <Box bg="red.500" minH="100vh"> */}
        <BrowserRouter>
          <App />
        </BrowserRouter>
      {/* </Box> */}
    </ChakraProvider>
    </GoogleOAuthProvider>
  </StrictMode>
);