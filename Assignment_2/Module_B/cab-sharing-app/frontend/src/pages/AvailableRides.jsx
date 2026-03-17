import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box, Flex, Text, Avatar, Button, VStack, HStack, Badge, Collapse, Icon
} from '@chakra-ui/react';

// --- Sub-component: A single Ride Card ---
const RideCard = ({ ride }) => {
    const [showDetails, setShowDetails] = useState(false);
    const navigate = useNavigate();

    // Format the date to match the image: "10:00 (20 Nov)"
    const formatTime = (dateString) => {
        const date = new Date(dateString);
        const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const dayMonth = date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
        return `${time} (${dayMonth})`;
    };

    return (
        <Box 
            borderWidth="1px" 
            borderColor="gray.100" 
            borderRadius="2xl" 
            p={5} 
            mb={5} 
            bg="white" 
            boxShadow="sm"
            transition="all 0.2s"
            _hover={{ boxShadow: 'md' }}
        >
            {/* 1. Header: Host Info & Seats */}
            <Flex justify="space-between" align="center" mb={6}>
                <HStack spacing={3}>
                    <Avatar 
                        src={ride.ProfileImageURL} 
                        size="md" 
                        cursor="pointer" 
                        onClick={() => navigate(`/profile/${ride.AdminID}`)}
                    />
                    <VStack align="start" spacing={0}>
                        <Text fontSize="xs" fontWeight="bold" color="gray.400" letterSpacing="wider">
                            HOST
                        </Text>
                        <Text 
                            fontSize="md" 
                            fontWeight="bold" 
                            color="gray.800"
                            cursor="pointer"
                            _hover={{ textDecoration: 'underline' }}
                            onClick={() => navigate(`/profile/${ride.AdminID}`)}
                        >
                            {ride.HostName}
                        </Text>
                    </VStack>
                </HStack>
                
                {/* Seats Left Badge matching the image style */}
                <Badge 
                    bg="green.50" 
                    color="green.600" 
                    px={3} 
                    py={1} 
                    borderRadius="full" 
                    textTransform="none" 
                    fontSize="sm"
                    fontWeight="semibold"
                >
                    {ride.AvailableSeats} seats left
                </Badge>
            </Flex>

            {/* 2. Visual Timeline: Source to Destination */}
            <Flex mb={6}>
                {/* The Dots and Line */}
                <VStack spacing={0} align="center" mr={4} mt={1}>
                    {/* Source Dot */}
                    <Box w="12px" h="12px" borderRadius="full" bg="gray.200" display="flex" alignItems="center" justifyContent="center">
                        <Box w="6px" h="6px" borderRadius="full" bg="gray.400" />
                    </Box>
                    {/* Connecting Line */}
                    <Box w="2px" h="30px" bg="gray.100" />
                    {/* Destination Dot */}
                    <Box w="16px" h="16px" borderRadius="full" bg="green.100" display="flex" alignItems="center" justifyContent="center">
                        <Box w="6px" h="6px" borderRadius="full" bg="green.400" />
                    </Box>
                </VStack>

                {/* The Locations */}
                <VStack align="start" spacing={5}>
                    <Text fontSize="md" color="gray.600">{ride.Source}</Text>
                    <Text fontSize="md" fontWeight="bold" color="gray.900">{ride.Destination}</Text>
                </VStack>
            </Flex>

            {/* 3. Time and Date */}
            <HStack color="gray.500" mb={6} fontSize="sm">
                <Box as="span" mr={1}>🕒</Box>
                <Text>{formatTime(ride.StartTime)}</Text>
            </HStack>

            {/* 4. Action Buttons */}
            <Flex gap={3} mb={showDetails ? 4 : 0}>
                <Button 
                    flex={1} 
                    variant="outline" 
                    borderColor="gray.200" 
                    color="gray.700" 
                    borderRadius="xl"
                    _hover={{ bg: 'gray.50' }}
                >
                    💬 Chat
                </Button>
                <Button 
                    flex={1} 
                    bg="#141b2d" 
                    color="white" 
                    borderRadius="xl"
                    _hover={{ bg: 'gray.800' }}
                >
                    Request {'>'}
                </Button>
            </Flex>

            {/* Details Toggle Button (Centered at bottom) */}
            <Flex justify="center" mt={showDetails ? 0 : 4}>
                <Button 
                    size="sm" 
                    variant="ghost" 
                    color="gray.400" 
                    onClick={() => setShowDetails(!showDetails)}
                >
                    {showDetails ? 'Hide details ᐱ' : 'More details ᐯ'}
                </Button>
            </Flex>

            {/* 5. Hidden Extra Details Section */}
            <Collapse in={showDetails} animateOpacity>
                <Box mt={2} p={4} bg="gray.50" borderRadius="lg" fontSize="sm" color="gray.700">
                    <Flex justify="space-between" mb={2}>
                        <Text color="gray.500">Vehicle Type</Text>
                        <Text fontWeight="medium">{ride.VehicleType}</Text>
                    </Flex>
                    <Flex justify="space-between" mb={2}>
                        <Text color="gray.500">Est. Duration</Text>
                        <Text fontWeight="medium">{ride.EstimatedTime} mins</Text>
                    </Flex>
                    <Flex justify="space-between" mb={2}>
                        <Text color="gray.500">Total Passengers</Text>
                        <Text fontWeight="medium">{ride.PassengerCount}</Text>
                    </Flex>
                    {ride.FemaleOnly && (
                        <Flex justify="space-between" mt={3} pt={3} borderTop="1px solid" borderColor="gray.200">
                            <Text color="pink.500" fontWeight="bold">♀ Female Only Ride</Text>
                            <Text color="gray.500">Safety Policy</Text>
                        </Flex>
                    )}
                </Box>
            </Collapse>
        </Box>
    );
};

// --- Main Page Component ---
const AvailableRides = () => {
    const [rides, setRides] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // MOCK API RESPONSE 
        // Notice: Added HostName and ProfileImageURL (Simulating a SQL JOIN with the Members table)
        const mockRidesFromAPI = [
            {
                RideID: 101,
                AdminID: 42,
                HostName: "Aditi Sharma",
                ProfileImageURL: "https://bit.ly/dan-abramov", 
                PassengerCount: 1,
                AvailableSeats: 2,
                Source: "IITGN Housing Block",
                Destination: "Ahmedabad Airport (AMD)",
                VehicleType: "Sedan (Swift Dzire)",
                StartTime: "2023-11-20T10:00:00",
                EstimatedTime: 45,
                FemaleOnly: false
            },
            {
                RideID: 102,
                AdminID: 88,
                HostName: "Priya Patel",
                ProfileImageURL: "https://bit.ly/kent-c-dodds",
                PassengerCount: 3,
                AvailableSeats: 1,
                Source: "Library Gate",
                Destination: "Gandhinagar Railway Station",
                VehicleType: "Auto Rickshaw",
                StartTime: "2023-11-20T18:30:00",
                EstimatedTime: 20,
                FemaleOnly: true
            }
        ];

        setTimeout(() => {
            setRides(mockRidesFromAPI);
            setLoading(false);
        }, 1000);
    }, []);

    return (
        <Box maxW="600px" mx="auto" p={5}>
            <Text fontSize="2xl" fontWeight="bold" mb={6} color="gray.800">
                Available Rides
            </Text>

            {loading ? (
                <Text color="gray.500">Loading rides from server...</Text>
            ) : (
                <Box>
                    {rides.length === 0 ? (
                        <Text color="gray.500">No active rides found right now.</Text>
                    ) : (
                        rides.map(ride => <RideCard key={ride.RideID} ride={ride} />)
                    )}
                </Box>
            )}
        </Box>
    );
};

export default AvailableRides;