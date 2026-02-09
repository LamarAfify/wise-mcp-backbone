import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Users,
    Target,
    Calendar,
    CheckCircle,
    Clock,
    BarChart2,
    Briefcase
} from 'lucide-react';

const API_URL = 'http://localhost:8001';

export default function Dashboard() {
    const [data, setData] = useState({ projects: [], users: [], milestones: [] });
    const [recommendation, setRecommendation] = useState(null);
    const [selectedTaskType, setSelectedTaskType] = useState('analytics');

    useEffect(() => {
        fetch(`${API_URL}/dashboard`)
            .then(res => res.json())
            .then(setData)
            .catch(console.error);
    }, []);

    const getRecommendation = (projectId, taskType) => {
        fetch(`${API_URL}/recommend/${projectId}/${taskType}`)
            .then(res => res.json())
            .then(res => setRecommendation({ user_id: res.recommended_user_id, task_type: taskType }))
            .catch(console.error);
    };

    const toggleMilestone = (id, currentStatus) => {
        if (currentStatus === 'completed') return;
        fetch(`${API_URL}/milestones/${id}/complete`, { method: 'POST' })
            .then(() => {
                setData(prev => ({
                    ...prev,
                    milestones: prev.milestones.map(m =>
                        m.id === id ? { ...m, status: 'completed' } : m
                    )
                }));
            })
            .catch(console.error);
    };

    // Show the most recently created project
    const project = data.projects.length > 0 ? data.projects[data.projects.length - 1] : null;

    if (!project) return (
        <div className="flex flex-col items-center justify-center h-64 text-gray-400 glass-panel m-8">
            <h2 className="text-xl font-semibold mb-2">Ready for Onboarding</h2>
            <p>Ask North AI to start a new project...</p>
        </div>
    );

    return (
        <div className="p-8 max-w-6xl mx-auto space-y-8">
            {/* Header */}
            <header className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-teal-300">
                        {project.name}
                    </h1>
                    <p className="text-gray-400 mt-2 flex items-center gap-2">
                        <Calendar size={16} /> Due: {new Date(project.deadline).toLocaleDateString()}
                    </p>
                </div>
                <div className="flex -space-x-3">
                    {data.users.map(u => (
                        <div key={u.id} className="w-10 h-10 rounded-full bg-slate-700 border-2 border-slate-900 flex items-center justify-center text-xs font-bold" title={u.name}>
                            {u.name.substring(0, 2).toUpperCase()}
                        </div>
                    ))}
                </div>
            </header>

            {/* Tracker Bars (Milestones) */}
            <section className="glass-panel p-6">
                <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <Target className="text-teal-400" /> Project Milestones
                </h2>
                <div className="space-y-6">
                    {data.milestones.map(m => (
                        <div key={m.id} className="space-y-2">
                            <div className="flex justify-between text-sm items-center">
                                <span className="font-medium text-gray-200">{m.title}</span>
                                <div className="flex items-center gap-3">
                                    <span className={`px-2 py-0.5 rounded text-xs ${m.status === 'completed' ? 'bg-green-900/50 text-green-300' :
                                        m.status === 'in_progress' ? 'bg-blue-900/50 text-blue-300' :
                                            'bg-gray-800 text-gray-400'
                                        }`}>
                                        {m.status.replace('_', ' ').toUpperCase()}
                                    </span>
                                    {m.status !== 'completed' && (
                                        <button
                                            onClick={() => toggleMilestone(m.id, m.status)}
                                            className="text-gray-500 hover:text-green-400 transition-colors"
                                            title="Mark as Complete"
                                        >
                                            <CheckCircle size={18} />
                                        </button>
                                    )}
                                </div>
                            </div>
                            <div className="tracker-bar-container">
                                <motion.div
                                    className={`tracker-bar-fill ${m.status === 'completed' ? 'bg-green-500' :
                                        m.status === 'in_progress' ? 'bg-blue-500' :
                                            'bg-gray-700'
                                        }`}
                                    initial={{ width: 0 }}
                                    animate={{ width: m.status === 'completed' ? '100%' : m.status === 'in_progress' ? '50%' : '0%' }}
                                />
                            </div>
                            <div className="flex justify-between text-xs text-gray-500">
                                <span>Assignee: {data.users.find(u => u.id === m.assigned_to)?.name || 'Unassigned'}</span>
                                <span>Due: {m.due_date ? new Date(m.due_date).toLocaleDateString() : 'No date'}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Intelligent Assignment */}
            <section className="glass-panel p-6 bg-gradient-to-br from-indigo-900/20 to-purple-900/10">
                <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <Briefcase className="text-purple-400" /> Intelligent Task Assignment
                </h2>
                <div className="flex gap-4 items-end">
                    <div className="flex-1">
                        <label className="block text-sm text-gray-400 mb-2">Task Type</label>
                        <select
                            className="input-field"
                            value={selectedTaskType}
                            onChange={(e) => setSelectedTaskType(e.target.value)}
                        >
                            <option value="analytics">Data Analytics</option>
                            <option value="writing">Content Writing</option>
                            <option value="coding">Software Development</option>
                        </select>
                    </div>
                    <button
                        onClick={() => getRecommendation(project.id, selectedTaskType)}
                        className="btn btn-primary h-[48px]"
                    >
                        Find Best Match
                    </button>
                </div>

                {recommendation && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-6 p-4 rounded-lg bg-white/5 border border-purple-500/30 flex items-center gap-4"
                    >
                        <div className="p-3 rounded-full bg-purple-500/20 text-purple-300">
                            <Users size={24} />
                        </div>
                        <div>
                            <p className="text-sm text-gray-400">Recommended for <strong>{recommendation.task_type}</strong></p>
                            <p className="text-lg font-bold text-white">
                                {data.users.find(u => u.id === recommendation.user_id)?.name || 'Needs Onboarding'}
                            </p>
                        </div>
                    </motion.div>
                )}
            </section>

        </div>
    );
}
