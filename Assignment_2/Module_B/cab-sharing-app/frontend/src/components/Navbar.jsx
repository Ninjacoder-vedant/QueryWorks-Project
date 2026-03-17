import React from 'react';
import {
  Box,
  Flex,
  Avatar,
  HStack,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  useColorModeValue,
  Stack,
  Text,
} from '@chakra-ui/react';
import { Link as RouterLink, useLocation, useNavigate } from 'react-router-dom';

// 1. Updated NavLink to support "Active" state highlighting
const NavLink = ({ children, to }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Box
      as={RouterLink}
      to={to}
      px={3}
      py={2}
      rounded="md"
      // Change font weight and colors if active
      fontWeight={isActive ? 'bold' : 'medium'}
      color={isActive ? useColorModeValue('blue.600', 'blue.300') : useColorModeValue('gray.600', 'gray.200')}
      bg={isActive ? useColorModeValue('blue.50', 'gray.700') : 'transparent'}
      _hover={{
        textDecoration: 'none',
        bg: useColorModeValue('gray.100', 'gray.700'),
      }}
      transition="all 0.2s ease"
    >
      {children}
    </Box>
  );
};

export default function Navbar() {
  const navigate = useNavigate();
  // We can check localStorage directly here to keep the Navbar self-contained
  const isLoggedIn = localStorage.getItem('isAuthenticated') === 'true';

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    navigate('/login');
  };

  return (
    <Box bg={useColorModeValue('white', 'gray.900')} px={8} boxShadow="sm" borderBottom={1} borderStyle="solid" borderColor={useColorModeValue('gray.200', 'gray.700')}>
      <Flex h={16} alignItems="center" justifyContent="space-between">

        {/* Left Side: Logo and Navigation Links */}
        <HStack spacing={8} alignItems="center">
          <Box as={RouterLink} to={isLoggedIn ? "/available-rides" : "/login"}>
            <Text fontSize="xl" fontWeight="bold" color="blue.500" letterSpacing="tight">
              CampusRide
            </Text>
          </Box>

          {/* Only show these links if logged in */}
          {isLoggedIn && (
            <HStack as="nav" spacing={2} display={{ base: 'none', md: 'flex' }}>
              <NavLink to="/available-rides">Available Rides</NavLink>
              <NavLink to="/create-ride">Create Ride</NavLink>
              <NavLink to="/your-rides">Your Rides</NavLink>
              <NavLink to="/ride-history">Ride History</NavLink>
            </HStack>
          )}
        </HStack>

        {/* Right Side: Profile Menu OR Login/Signup Buttons */}
        <Flex alignItems="center">
          {isLoggedIn ? (
            <Menu>
              <MenuButton as={Button} rounded="full" variant="link" cursor="pointer" minW={0}>
                <Avatar
                  size="sm"
                  src="https://images.unsplash.com/photo-1493666438817-866a91353ca9?ixlib=rb-0.3.5&q=80&fm=jpg&crop=faces&fit=crop&h=200&w=200&s=b616b2c5b373a80ffc9636ba24f7a4a9"
                />
              </MenuButton>
              <MenuList>
                <MenuItem onClick={() => navigate("/Profile")}>
                  Profile
                </MenuItem>
                <MenuItem>Settings</MenuItem>
                <MenuDivider />
                <MenuItem onClick={handleLogout} color="red.500" fontWeight="semibold">
                  Logout
                </MenuItem>
              </MenuList>
            </Menu>
          ) : (
            // The Logged-Out State
            <Stack direction="row" spacing={4} align="center">
              <Button as={RouterLink} to="/login" variant="ghost" colorScheme="blue" fontWeight="medium">
                Log in
              </Button>
              <Button as={RouterLink} to="/signup" colorScheme="blue" fontWeight="medium">
                Sign Up
              </Button>
            </Stack>
          )}
        </Flex>
      </Flex>
    </Box>
  );
}