import React, { useState }from 'react'
import {
  Divider,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  Box,
  Select,
  Input,
  FormLabel,
  Button,
  Stack,
  VStack,
  RadioGroup,
  Radio,
  Text,
  HStack
} from '@chakra-ui/react'
import { useColorMode } from '@chakra-ui/color-mode';
import { useEffect } from 'react';
import axios from 'axios';

export default function QuickStatement(props) {
  
  const [autoSelection, setAutoSelection] = useState(false);
  const [currentRadio, setCurrentRadio] = useState(null);
  const [client, setClient] = useState('');
  const [startdate, setStartdate] = useState(new Date());
  const [enddate, setEnddate] = useState(new Date());
  const [events, setEvents] = useState([]);

  const stateStr = window.sessionStorage.getItem('persist:root');
  const state = JSON.parse(stateStr);
  const user = JSON.parse(state.user);
  const token = JSON.parse(state.token);
  const clients = JSON.parse(state.clients);
  const allEvents = JSON.parse(state.events);

  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  const makeStatement = async () => {
    const response = await axios.post(`/client/makestatement`, {
      user: user,
      token: token,
      client: JSON.parse(client),
      currentRadio: currentRadio,
      startdate: startdate,
      enddate: enddate,
      events: allEvents
    })
    .then(response => console.log(response)
    .catch(err => console.log(err)))
  }

  useEffect(() => {
    console.log("client: \n" + client); 
    console.log("AllEvents: \n", allEvents);
    console.log("Events: \n", events)
  })

  return (
    <>
      <Drawer
        isOpen={props.statementDrawerOpen}
        placement="left"
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton onClick={() => { props.setStatementDrawerOpen(false) }}/>
          <DrawerHeader borderBottomWidth="1px">Quick Statement</DrawerHeader>

          <DrawerBody>
            <Stack spacing="24px" style={{marginTop: '2rem'}}>
              <Box>
              <Box>
                <FormLabel>Select Client</FormLabel>
                <Select onChange={(e) => {setClient(e.target.value); setEvents(allEvents.filter(event => event.clientID == client["_id"]));}}>
                  {clients.map(client => {return (
                        <option value={JSON.stringify(client)}>{client.fname + " " + client.lname}</option>
                      )}
                    )}
                </Select>
              </Box>
                <RadioGroup onClick={() => { setAutoSelection(true) }} onChange={(val) => {setCurrentRadio(val)}}style={{marginTop: '2rem'}}>
                  <VStack spacing={4} direction="row">
                    <Radio 
                      defaultChecked="false" 
                      isDisabled={autoSelection ? false : true} 
                      value="currentMonth"
                    >Current Month
                    </Radio>
                    <Radio 
                      defaultChecked="false" 
                      isDisabled={autoSelection ? false : true}
                      value="currentYear"
                    >Current Year
                    </Radio>
                  </VStack>
                </RadioGroup>
              </Box>
              <HStack>
                <Divider />
                  <h3>or</h3>
                <Divider />
              </HStack>
              <Stack spacing={4} direction="column"onClick={() => {setAutoSelection(false)}}>
                <Box>
                    <Text mb="8px">Start Date</Text>
                    <Input type="date" isDisabled={autoSelection ? true: false} onChange={(e) => {setStartdate(e.target.value)}}/>
                </Box>
                <Box>
                    <Text mb="8px">End Date</Text>
                    <Input type="date" isDisabled={autoSelection ? true: false} onChange={(e) => {setEnddate(e.target.value)}}/>
                </Box>
              </Stack>
            </Stack>
          </DrawerBody>

          <DrawerFooter >
            <Button style={{backgroundColor: isDark? "#63326E" : "#03b126", color: 'white'}} onClick={() => { makeStatement() }}>Download</Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </>
  )
}
