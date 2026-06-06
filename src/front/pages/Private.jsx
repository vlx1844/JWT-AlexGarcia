import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Private = () => {
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        const fetchPrivateData = async () => {
            try {
                const response = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/private", {
                    method: "GET",
                    headers: {
                        "Authorization": "Bearer " + token
                    }
                });

                if (response.status === 200) {
                    const data = await response.json();
                    setMessage(data.logged_in_as);
                } else {
                    sessionStorage.removeItem("token");
                    navigate("/login");
                }
            } catch (error) {
                console.error(error);
                sessionStorage.removeItem("token");
                navigate("/login");
            }
        };

        fetchPrivateData();
    }, []);

    return (
        <div className="container mt-5 text-center">
            <h2>Zona Privada</h2>
            {message ? <p>Bienvenido, {message}</p> : <p>Cargando...</p>}
            <button className="btn btn-danger mt-3" onClick={() => {
                sessionStorage.removeItem("token");
                navigate("/login");
            }}>
                Cerrar Sesión
            </button>
        </div>
    );
};