
import { useState } from 'react';
import Dashboard from './components/Dashboard';
import Onboarding from './components/Onboarding';

function App() {
  const [view, setView] = useState('dashboard');

  return (
    <div className="min-h-screen bg-[#0f1115] text-[#f3f4f6]">
      <nav className="p-6 flex justify-between items-center glass-panel m-4 mb-0">
        <div className="font-bold text-xl tracking-tight">NORTH <span className="text-teal-400">AI</span></div>
        <div className="space-x-4">
          <button
            onClick={() => setView('dashboard')}
            className={`text-sm ${view === 'dashboard' ? 'text-white font-semibold' : 'text-gray-400'}`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setView('onboarding')}
            className={`text-sm ${view === 'onboarding' ? 'text-white font-semibold' : 'text-gray-400'}`}
          >
            New Project
          </button>
        </div>
      </nav>

      {view === 'dashboard' ? <Dashboard /> : <Onboarding onComplete={() => setView('dashboard')} />}
    </div>
  );
}

export default App;
