import { Container } from '@chakra-ui/react'
import { Route, Routes } from 'react-router-dom'
import { UserPage } from './user/pages/UserPage'
import { PostPage } from './post/pages/PostPage'
import { Header } from './shared/components/Navigation/Header'
import AuthPage from './user/pages/AuthPage'

function App() {
  return (
    <Container maxW='620px'>
      <Header />
      <Routes>
        <Route path='/auth' element={<AuthPage />} />
        <Route path='/:username' element={<UserPage />} />
        <Route path='/:username/post/:pid' element={<PostPage />} />
      </Routes>
    </Container>
  )
}

export default App
