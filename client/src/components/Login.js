import React from "react";
import { useState } from "react";
import { useNavigate } from 'react-router-dom'
import { Input, Container, VStack, HStack, Button } from '@chakra-ui/react';
import { useDispatch } from 'react-redux';
import axios from "axios"
import { loginAction } from "../actions"
import { clientsAction } from '../actions';


export default function Login() {
// states for text input
const [username, setUsername] = useState("");
const [password, setPassword] = useState("");

const dispatch = useDispatch();
const navigate = useNavigate();

const loginUser = async (username, password) => {
    const configObject = {
        method: "POST",
        url: "http://localhost:3000/login",
        data: { username: username, password: password },
    };
    const response = await axios(configObject).catch(err => {console.error(err);})
    console.log(response.data)
    if (response.data) {
        dispatch(loginAction(response.data.user))
        dispatch(clientsAction(response.data.clients));
        navigate('/dashboard');
    } else {
        return <h1>err</h1>
    }
}

return (
    <Container style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <VStack className="loginCont" >
            <h3 className="willowCursive">Willow</h3>
            <Input className="textInput" placeholder="Email" type="email" variant='flushed' focusBorderColor="#03b126" onChange={(e) => {setUsername(e.target.value)}}/>
            <Input className="textInput" placeholder="Password" type="password" variant='flushed' focusBorderColor="#03b126" onChange={(e) => {setPassword(e.target.value)}}/>
            <HStack>
                <Button background="#03b126" color="#fff" onClick={() => {loginUser(username, password)}}>Login</Button>
                <Button background="#63326E" color="#fff">Register</Button>
            </HStack>
        </VStack>
    </Container>
)

}