
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, User, Calendar } from 'lucide-react';

const API_URL = 'http://localhost:8001';

export default function Onboarding({ onComplete }) {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        projectName: '',
        deadline: '',
        users: [{ name: '', role: 'member' }]
    });

    const addUserField = () => {
        setFormData({ ...formData, users: [...formData.users, { name: '', role: 'member' }] });
    };

    const updateUser = (index, field, value) => {
        const newUsers = [...formData.users];
        newUsers[index][field] = value;
        setFormData({ ...formData, users: newUsers });
    };

    const handleSubmit = async () => {
        try {
            // Create Project
            await fetch(`${API_URL}/projects`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id: `proj-${Date.now()}`,
                    name: formData.projectName,
                    deadline: formData.deadline,
                    status: 'active',
                    created_at: new Date().toISOString()
                })
            });

            // Create Users
            for (const user of formData.users) {
                if (user.name) {
                    await fetch(`${API_URL}/users`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            id: `user-${Date.now()}-${Math.random()}`,
                            name: user.name,
                            role: user.role,
                            skills: {}
                        })
                    });
                }
            }

            onComplete();
        } catch (error) {
            console.error('Onboarding failed:', error);
        }
    };

    return (
        <div className="max-w-2xl mx-auto py-12 px-6">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-panel p-8"
            >
                <h1 className="text-3xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500">
                    Welcome to North AI
                </h1>
                <p className="text-gray-400 mb-8">Let's set up your workflow hub.</p>

                {step === 1 && (
                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Project Name</label>
                            <input
                                type="text"
                                className="input-field"
                                placeholder="e.g. Q1 Marketing Campaign"
                                value={formData.projectName}
                                onChange={e => setFormData({ ...formData, projectName: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Deadline</label>
                            <div className="relative">
                                <Calendar className="absolute left-3 top-3 text-gray-500" size={18} />
                                <input
                                    type="date"
                                    className="input-field pl-10"
                                    value={formData.deadline}
                                    onChange={e => setFormData({ ...formData, deadline: e.target.value })}
                                />
                            </div>
                        </div>
                        <button
                            className="btn btn-primary w-full justify-center mt-4"
                            onClick={() => setStep(2)}
                        >
                            Next: Add Team
                        </button>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-6">
                        <div className="space-y-4">
                            {formData.users.map((user, idx) => (
                                <div key={idx} className="flex gap-4">
                                    <div className="relative flex-1">
                                        <User className="absolute left-3 top-3 text-gray-500" size={18} />
                                        <input
                                            type="text"
                                            className="input-field pl-10"
                                            placeholder="Team Member Name"
                                            value={user.name}
                                            onChange={e => updateUser(idx, 'name', e.target.value)}
                                        />
                                    </div>
                                    <select
                                        className="input-field w-32"
                                        value={user.role}
                                        onChange={e => updateUser(idx, 'role', e.target.value)}
                                    >
                                        <option value="member">Member</option>
                                        <option value="lead">Lead</option>
                                    </select>
                                </div>
                            ))}
                        </div>

                        <button
                            className="text-sm text-teal-400 flex items-center gap-1 hover:text-teal-300"
                            onClick={addUserField}
                        >
                            <Plus size={16} /> Add another member
                        </button>

                        <div className="flex gap-4 mt-8">
                            <button
                                className="btn bg-gray-700 text-white hover:bg-gray-600 flex-1 justify-center"
                                onClick={() => setStep(1)}
                            >
                                Back
                            </button>
                            <button
                                className="btn btn-primary flex-1 justify-center"
                                onClick={handleSubmit}
                            >
                                Launch Hub
                            </button>
                        </div>
                    </div>
                )}
            </motion.div>
        </div>
    );
}
