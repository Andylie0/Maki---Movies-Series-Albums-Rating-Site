import {useState, useEffect, useRef} from "react";

export const useOffline = () => {
    const [isOnline, setIsOnline] = useState(navigator.onLine);
    const [offlineQueue, setOfflineQueue] = useState([]);

    const offlineQueueRef = useRef(offlineQueue);

    useEffect(() => {
        offlineQueueRef.current = offlineQueue;
    }, [offlineQueue]);

    useEffect(() => {
        const handleOnline = () => {
            setIsOnline(true);
            syncWithServer();
        };
        const handleOffline = () => setIsOnline(false);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    const addToQueue = (action) => {
        setOfflineQueue(prev => [...prev, action]);
    };

    const syncWithServer = async () => {
        const queue = offlineQueueRef.current;
        for (const action of queue) {
            await fetch(`http://localhost:8000${action.url}`, {
                method: action.method,
                headers: action.headers,
                body: action.body,
            });
        }
        setOfflineQueue([]);
    };

    return { isOnline, addToQueue };
}