import React, { useState } from 'react';
import './App.scss';
import {
  FaCloud,
  FaCompass,
  FaMask,
  FaPaperPlane,
  FaRocket,
  FaShapes,
  FaShip,
  FaSkull,
  FaSnowman,
  FaStamp,
  FaStar,
  FaToolbox,
} from "react-icons/fa";
import hash from "hash.js";

const HASH = "2f6773a8ba969b009261bc2a1ff31bd15d892a4d9bd8fec8edf4754a75381971";

export default function App() {
  const [flag, setFlag] = useState(null);

  return (
    <div>
      {flag ? (
        <>
          <p>
            This challenge solution is actually based on a real-world
            vulnerability!
            <br />
            Yup. Someone actually screwed this up.
          </p>
          <p>{`HTM{${flag}}`}</p>
        </>
      ) : (
        <Login setFlagValue={setFlag} />
      )}
    </div>
  );
}

const icons = [
  FaCloud,
  FaCompass,
  FaMask,
  FaPaperPlane,
  FaRocket,
  FaShapes,
  FaShip,
  FaSkull,
  FaSnowman,
  FaStamp,
  FaStar,
  FaToolbox,
]

function Login({ setFlagValue }) {
  const [value, setValue] = useState("");

  function onChange(event) {
    setValue(event.target.value);
  }
  
  function click(event) {
    event.preventDefault();

    let v = hash.sha256().update(value).digest('hex');
    if (v === HASH) {
      let flag = hash.sha256().update("SALTY").update(value).digest('hex');
      setFlagValue(flag);
    } else {
      alert("wrong password!");
    }
  }

  const valueHash = hash.sha256().update(value).digest('hex');
  const h1 = parseInt(valueHash.slice(0, 8), 16) % icons.length;
  const h2 = parseInt(valueHash.slice(8, 16), 16) % icons.length;
  const h3 = parseInt(valueHash.slice(16, 24), 16) % icons.length;
  const c1 = 360 * parseInt(valueHash.slice(24, 28), 16) / 65535;
  const c2 = 360 * parseInt(valueHash.slice(28, 32), 16) / 65535;
  const c3 = 360 * parseInt(valueHash.slice(32, 36), 16) / 65535;
  
  return (
    <div className="login-container">
      <div className="login">
        <form className="form">
          <label htmlFor="secret">Secret Key</label>
          <input
            type="password"
            name="secret"
            value={value}
            onChange={onChange}
          />
          <input type="submit" value="Verify" onClick={click} />
        </form>

        {value !== "" && (
          <div className="identicons">
            <span style={{ color: `hsl(${c1}, 70%, 50%)` }}>{icons[h1]()}</span>
            <span style={{ color: `hsl(${c2}, 70%, 50%)` }}>{icons[h2]()}</span>
            <span style={{ color: `hsl(${c3}, 70%, 50%)` }}>{icons[h3]()}</span>
          </div>
        )}
      </div>

      <a href="/demo.mp4">see demo</a>
    </div>
  );
}
