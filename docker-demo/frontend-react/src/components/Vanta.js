import React, {useCallback, useEffect, useRef} from "react";
import styles from "./index.module.css";
import {useMediaQuery} from 'react-responsive'

const loadScriptAsync = (src) => new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
});

export function VantaBackground({children}) {
    const vantaRenderElement = useRef(null);
    // const isDesktopOrLaptop = useMediaQuery({
    //     query: '(min-width: 1224px)'
    // })
    // const isBigScreen = useMediaQuery({ query: '(min-width: 1824px)' })
    // const isPortrait = useMediaQuery({ query: '(orientation: portrait)' })
    // const isRetina = useMediaQuery({ query: '(min-resolution: 2dppx)' })
    const isTabletOrMobile = useMediaQuery({query: '(max-width: 1224px)'})


    const loadVantaScript = useCallback(async () => {
        try {
            await loadScriptAsync('https://cdnjs.cloudflare.com/ajax/libs/three.js/r121/three.min.js');
            await loadScriptAsync('https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js');
        } catch (e) {
            console.error(e);
        }
    }, []);

    useEffect(() => {
        loadVantaScript().then(() => {
            let options = {
                el: vantaRenderElement.current,
                baseColor: 0x6cc866,
                backgroundColor: "#272936",
                mouseControls: false,
                touchControls: false,
                gyroControls: false,
                xOffset: 0.0,
            }
            if (isTabletOrMobile) {
                options = {...{size: 0.7, yOffset: 0.32}, ...options}
            } else {
                options = {...{size: 1.0, yOffset: 0.28}, ...options}
            }
            window.VANTA.NET(options)

        });
    }, [loadVantaScript, vantaRenderElement, isTabletOrMobile]);


    return (
        <div ref={vantaRenderElement} className={styles.vanta}>
            {children}
        </div>
    );
}