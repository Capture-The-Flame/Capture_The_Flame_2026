'use client'

import Image from "next/image";
import { use, useState } from "react";
import { Box, Button, Stack, TextField, Typography } from "@mui/material";
import { useRouter } from 'next/navigation';

export default function Home() {

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'You can begin the challenge whenever you are ready, best of luck!',
    },
  ])

  const [message, setMessage] = useState('')

  // new helper function 

  const sendMessage = async () => {

    const userMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let botMessage = { role: 'assistant', content: '' };
      setMessages(prev => [...prev, botMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        botMessage.content += chunk;
        setMessages(prev => [...prev.slice(0, -1), { ...botMessage }]);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      // setIsLoading(false);
    }
    setMessage('')
  };

  const useEnterKeyToSend = (event) => {
    if (event.key === 'Enter') {
      sendMessage()
    }
  };
  

  return (
    <Box width="100vw" height="100vh" display="flex" flexDirection="column" justifyContent="center" alignItems="center"
      sx={{backgroundImage: 'url(/hearts101.jpg)', backgroundSize: 'cover', backgroundPosition: 'center',}}>

      <Stack direction="column" width="95vw" height="95vh" p={2} spacing={3}>
        <Stack direction="column" spacing={2} flexGrow={1} overflow="auto" maxHeight="100%">
          {
            messages.map((t_message, index) => {
              return (
                <Box key={index} display="flex" justifyContent = {t_message.role === 'assistant' ? 'flex-start' : 'flex-end'}>
                  <Box bgcolor={t_message.role === 'assistant' ? '#ff0000' : '#f00074'} color="white" borderRadius={16} p={3}>
                    { t_message.content } 
                  </Box>
                </Box>
              )
            })
          }
        </Stack>
        <Stack direction="row" spacing={2}>
          <TextField label="Converse with Mr Darcy" fullWidth InputProps={{sx: {backgroundColor: "#df6262", }}} value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={useEnterKeyToSend}>
          </TextField>
          <Button variant="contained" color="error" onClick={sendMessage}>Ask</Button>
          {/* <Button variant="contained" color="success" href="mailto:sufiyanretreat@gmail.com">Submit</Button> */}
        </Stack>
      </Stack>
    </Box>
  )
}