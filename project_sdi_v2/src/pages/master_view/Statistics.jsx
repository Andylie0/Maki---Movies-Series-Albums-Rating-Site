import MakiLogo from "../../assets/MAKI.png";
import ProfileIcon from "../../assets/profile_img.png";
import './Statistics.css'
import {useState} from "react";
import ParticlesBackground from './Particles.jsx'
import {useNavigate} from "react-router-dom";
import {BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend } from 'recharts';


export default function Statistics({allReviews, allMovies}) {
    const nav = useNavigate();

    const [activePage, setActivePage] = useState("journal")
    const [activeTab, setActiveTab] = useState("stats")

    const [searchInput, setSearchInput] = useState("");

    // Bar chart data - count reviews per rating
    const ratingData = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5].map(r => ({
        rating: r,
        count: allReviews.filter(review => review.rating === r).length
    }))

    // Pie chart data - count by type
    const typeCount = allReviews.reduce((acc, review) => {
        const movie = allMovies.find(m => m.id === review.movie_id)
        const type = movie?.type || "Unknown"
        acc[type] = (acc[type] || 0) + 1
        return acc
    }, {})

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const { name, value } = payload[0]
            const total = allReviews.length
            const percent = ((value / total) * 100).toFixed(0)
            return (
                <div className="custom-tooltip">
                    <p>{name}: {value}, {percent}%</p>
                </div>
            )
        }
        return null
    }

    function handleSearchNav() {
        const movie = allMovies.find(movie => movie.name.toLowerCase().includes(searchInput.toLowerCase()))
        if(movie)
            nav(`/details/${movie.id}`)
    }

    const typeData = Object.entries(typeCount).map(([name, value]) => ({ name, value }))
    const COLORS = ['#C0522A', '#C98B1F', '#FFCE27']

    function handleTable(){
        nav("/journal");
    }

    const suggestions = searchInput.length > 0
        ? allMovies.filter(m =>
            m.name.toLowerCase().includes(searchInput.toLowerCase())
        ).slice(0, 3)
        : []

    return(
        <div className="stats">
            <ParticlesBackground colour="#EB4144"/>
            <header className="stats-header">
                <img src = {MakiLogo} alt= "logo_maki" className="logo-maki"/>
                <div className="search-bar">
                    <input type="text" placeholder="Search..." className="search-input"
                           onChange={(e) => setSearchInput(e.target.value)}
                           onKeyDown={(e) => e.key === 'Enter' && handleSearchNav()}
                    />
                    <button className="search-icon" onClick={handleSearchNav}>🔍︎</button>

                    {suggestions.length > 0 && (
                        <div className="search-dropdown">
                            {suggestions.map(movie => (
                                <div key={movie.id} className="search-suggestion"
                                     onClick={() => {
                                         setSearchInput("")
                                         nav(`/details/${movie.id}`)
                                     }}>
                                    <img src={movie.image} alt={movie.name} />
                                    <div>
                                        <p className="suggestion-name">{movie.name}</p>
                                        <p className="suggestion-year">{movie.year_released}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
                <button className={`journal-button-header ${activePage ==="journal" ? "active" : ""}`}
                        onClick={() => setActivePage("journal")}>Journal</button>
                <button className={`watchlist-button-header ${activePage === "watchlist" ? "active" : ""}`}
                        onClick={() => setActivePage("watchlist")}>Watchlist</button>
                <img src ={ProfileIcon} alt= "user_icon" className="user-icon"/>
            </header>

            <main>
                <div className="button-section">
                    <button className={`table-button ${activeTab === "table" ? "active" : ""}`}
                            onClick={() =>{ setActiveTab("table"); handleTable()}}>Table</button>
                    <button className={`stats-button ${activeTab === "stats" ? "active" : ""}`}
                            onClick={() => {setActiveTab("stats")}}>Statistics</button>
                </div>

                <div className="rating-distribution">
                    <p>Rating distribution</p>
                    <p>{allReviews.length}</p>
                </div>

                <div className="charts-container">
                    <div className="bar-chart-wrapper">
                        <span className="star-label">★</span>
                        <BarChart width={900} height={220} data={ratingData} margin={{ top: 20, right: 0, left: 0, bottom: 10 }}>
                            <XAxis dataKey="rating" axisLine={{ stroke: '#ffffff', strokeWidth : 2}} tickLine={false} tick={false}/>
                            <YAxis hide={true} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#E2AC17"  radius={[6, 6, 6, 6]}
                                 stroke="#000000"
                                 strokeWidth={2}
                                 minPointSize={15}/>
                        </BarChart>
                        <span className="star-label">★★★★★</span>
                    </div>

                    <PieChart width={600} height={400}>
                        <Pie
                            data={typeData}
                            dataKey="value"
                            nameKey="name"
                            outerRadius={150}
                            stroke = "none"
                        >
                            {typeData.map((_, i) => (
                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip content={CustomTooltip} />
                    </PieChart>
                </div>
            </main>
        </div>
    )
}