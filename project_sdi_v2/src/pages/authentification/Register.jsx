import {useNavigate} from "react-router-dom"
import './Register.css'
import MakiLogo from "../../assets/MAKI.png";


export default function Register() {
    const navigate = useNavigate();

    function handleSignUp() {
        navigate('/journal');
    }

    function handleLogin(){
        navigate('/');
    }

    return(
        <div className="register-container">
            <div className="image-title">
                <img src = {MakiLogo} alt= "logo_maki" className="logo-maki"/>
                <h1>We are glad to have you!</h1>
            </div>
            <div className = "combo-signup">
                <div className="mail">
                    <p>Mail: </p>
                    <input type="text" placeholder="Type your mail here..." />
                </div>
                <div className="user">
                    <p>Username: </p>
                    <input type="text" placeholder="Type your username here..." />
                </div>
                <div className="password">
                    <p>Password: </p>
                    <input type="password" placeholder="Type your password here..."/>
                </div>
                <div className="password">
                    <p>Confirm Password: </p>
                    <input type="password" placeholder="Rewrite your password here..."/>
                </div>
                <div className="signup-section">
                    <button className="register-button" onClick={() => handleSignUp()}>Register!</button>
                    <span className="login-link" onClick={() => handleLogin()}>Already have an account? Back to log in.</span>
                </div>
            </div>
        </div>
    )
}