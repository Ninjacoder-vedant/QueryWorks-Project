import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box, Flex, Avatar, Text, Button, VStack, HStack, Divider,
  Stat, StatLabel, StatNumber, StatGroup, Icon, Badge
} from '@chakra-ui/react';

const Profile = () => {
  // Grab the ID from the URL (e.g., /profile/42 -> id is "42")
  const { id } = useParams(); 
  
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  // MOCK: Pretend the currently logged-in user has MemberID = 1
  const myMemberId = "1"; 
  
  // If there is no ID in the URL, or the ID matches my ID, it's MY profile.
  const isOwnProfile = !id || id === myMemberId;

  useEffect(() => {
    // MOCK API FETCH: In reality, you would fetch from your FastAPI backend
    // fetch(`http://localhost:8000/profile/${id ? id : 'me'}`)
    
    setTimeout(() => {
      const mockData = {
        MemberID: isOwnProfile ? 1 : parseInt(id),
        FullName: isOwnProfile ? "Student User" : "Aditi Sharma",
        ProfileImageURL: isOwnProfile ? "" : "https://bit.ly/dan-abramov",
        Programme: "B.Tech",
        Branch: "Computer Science",
        BatchYear: 2026,
        Email: isOwnProfile ? "student.user@iitgn.ac.in" : "Hidden (Private)",
        ContactNumber: isOwnProfile ? "+91 9876543210" : "Hidden (Private)",
        Age: 20,
        Gender: "F",
        // Stats from the MemberStats table
        AverageRating: 4.8,
        TotalRidesTaken: 12,
        TotalRidesHosted: 5,
        NumberOfRatings: 8
      };
      setProfile(mockData);
      setLoading(false);
    }, 800);
  }, [id, isOwnProfile]);

  if (loading) return <Text p={5}>Loading profile...</Text>;

  return (
    <Box maxW="800px" mx="auto" p={5}>
      <Box bg="white" p={8} borderRadius="2xl" boxShadow="sm" borderWidth="1px" borderColor="gray.100">
        
        {/* --- Header: Avatar and Basic Info --- */}
        <Flex direction={{ base: "column", sm: "row" }} align="center" justify="space-between">
          <HStack spacing={6}>
            <Avatar size="2xl" src={profile.ProfileImageURL} name={profile.FullName} />
            <VStack align="start" spacing={1}>
              <Text fontSize="2xl" fontWeight="bold" color="gray.800">
                {profile.FullName}
              </Text>
              <Text color="gray.500" fontSize="md" fontWeight="medium">
                {profile.Programme} • {profile.Branch} • Class of {profile.BatchYear}
              </Text>
              <Badge colorScheme={profile.Gender === 'F' ? 'pink' : 'blue'} mt={2} borderRadius="full" px={3}>
                Age: {profile.Age}
              </Badge>
            </VStack>
          </HStack>

          {/* Action Button Changes based on ownership */}
          <Box mt={{ base: 4, sm: 0 }}>
            {isOwnProfile ? (
              <Button colorScheme="blue" variant="outline" borderRadius="xl">
                Edit Profile
              </Button>
            ) : (
              <Button bg="#141b2d" color="white" _hover={{ bg: 'gray.800' }} borderRadius="xl">
                Message Host
              </Button>
            )}
          </Box>
        </Flex>

        <Divider my={8} borderColor="gray.200" />

        {/* --- Stats Section (From MemberStats Table) --- */}
        <Box bg="gray.50" p={5} borderRadius="xl" mb={8}>
          <Text fontSize="sm" fontWeight="bold" color="gray.400" mb={4} letterSpacing="wider">
            RIDE STATISTICS
          </Text>
          <StatGroup>
            <Stat>
              <StatLabel color="gray.600">Avg Rating</StatLabel>
              <StatNumber fontSize="2xl" color="gray.800">⭐ {profile.AverageRating}</StatNumber>
              <Text fontSize="xs" color="gray.500">({profile.NumberOfRatings} reviews)</Text>
            </Stat>
            <Stat>
              <StatLabel color="gray.600">Rides Hosted</StatLabel>
              <StatNumber fontSize="2xl" color="gray.800">{profile.TotalRidesHosted}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel color="gray.600">Rides Taken</StatLabel>
              <StatNumber fontSize="2xl" color="gray.800">{profile.TotalRidesTaken}</StatNumber>
            </Stat>
          </StatGroup>
        </Box>

        {/* --- Private/Contact Details --- */}
        <Text fontSize="sm" fontWeight="bold" color="gray.400" mb={4} letterSpacing="wider">
          CONTACT INFORMATION
        </Text>
        <VStack align="start" spacing={4}>
          <Flex w="100%" justify="space-between" borderBottom="1px solid" borderColor="gray.100" pb={2}>
            <Text color="gray.500">Email Address</Text>
            <Text fontWeight="medium" color={isOwnProfile ? "gray.800" : "gray.400"}>
              {profile.Email}
            </Text>
          </Flex>
          <Flex w="100%" justify="space-between" borderBottom="1px solid" borderColor="gray.100" pb={2}>
            <Text color="gray.500">Contact Number</Text>
            <Text fontWeight="medium" color={isOwnProfile ? "gray.800" : "gray.400"}>
              {profile.ContactNumber}
            </Text>
          </Flex>
        </VStack>

      </Box>
    </Box>
  );
};

export default Profile;