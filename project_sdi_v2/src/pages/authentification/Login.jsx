import { useNavigate } from 'react-router-dom'
import './Login.css'
import MakiLogo from '../../assets/MAKI.png'

export function Login(){
    const navigate = useNavigate();

    const handleLogin = () => {
        navigate("/journal");
    }

    const handleRegister = () => {
        navigate("/register");
    }

    return(
        <div className="login-container">
            <div className="image-title">
                <img src = {MakiLogo} alt= "logo_maki" className="logo-maki"/>
                <h1>Welcome to Maki!</h1>
            </div>
            <div className = "mail-pass-login-combo">
                <div className="mail">
                    <p>Mail: </p>
                    <input type="text" placeholder="Type your mail here..." />
                </div>
                <div className="password">
                    <p>Password: </p>
                    <input type="password" placeholder="Type your password here..."/>
                    <span className="forgot-password">Forgot Password?</span>
                </div>
                <div className="login-section">
                    <button className="login-button" onClick={() => handleLogin()}>Log in!</button>
                    <span className="signup-link" onClick={() => handleRegister()}>Don’t have an account? Sign up</span>
                </div>
            </div>
        </div>
    )
}

export default Login