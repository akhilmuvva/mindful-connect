import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import { db } from '../../services/firebase';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { toast } from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

const MOODS = [
    { value: 1, label: 'Very Low', emoji: '😢', color: 'bg-red-100 text-red-600 border-red-200' },
    { value: 2, label: 'Low', emoji: '😕', color: 'bg-orange-100 text-orange-600 border-orange-200' },
    { value: 3, label: 'Neutral', emoji: '😐', color: 'bg-yellow-100 text-yellow-600 border-yellow-200' },
    { value: 4, label: 'Good', emoji: '🙂', color: 'bg-blue-100 text-blue-600 border-blue-200' },
    { value: 5, label: 'Excellent', emoji: '😄', color: 'bg-green-100 text-green-600 border-green-200' },
];

const TRIGGERS = [
    'Work', 'Sleep', 'Family', 'Friends', 'Health', 'Weather', 'Food', 'Exercise', 'Stress', 'Relaxation'
];

export default function MoodLogger() {
    const [mood, setMood] = useState(3);
    const [selectedTriggers, setSelectedTriggers] = useState([]);
    const [note, setNote] = useState('');
    const [loading, setLoading] = useState(false);

    const { currentUser } = useAuth();
    const navigate = useNavigate();

    const handleTriggerToggle = (trigger) => {
        if (selectedTriggers.includes(trigger)) {
            setSelectedTriggers(selectedTriggers.filter(t => t !== trigger));
        } else {
            setSelectedTriggers([...selectedTriggers, trigger]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!currentUser) return;

        setLoading(true);
        try {
            await addDoc(collection(db, 'mood_logs'), {
                userId: currentUser.uid,
                moodValue: mood,
                moodLabel: MOODS.find(m => m.value === mood)?.label || 'Unknown',
                triggers: selectedTriggers,
                note,
                createdAt: serverTimestamp(),
            });

            toast.success('Mood logged successfully! 🎉');
            navigate('/dashboard');
        } catch (error) {
            console.error("Error logging mood:", error);
            toast.error('Failed to log mood. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-8 p-4">
            <div className="text-center">
                <h2 className="text-3xl font-bold text-slate-800">How are you feeling?</h2>
                <p className="text-slate-500 mt-2">Take a moment to check in with yourself.</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8 bg-white p-8 rounded-2xl shadow-sm border border-slate-100">

                {/* Mood Slider/Selection */}
                <div className="space-y-4">
                    <label className="block text-sm font-medium text-slate-700">Select your mood</label>
                    <div className="flex justify-between gap-2">
                        {MOODS.map((m) => (
                            <motion.button
                                key={m.value}
                                type="button"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => setMood(m.value)}
                                className={`flex-1 flex flex-col items-center p-3 rounded-xl border-2 transition-all ${mood === m.value
                                        ? m.color + ' ring-2 ring-offset-2 ring-blue-500'
                                        : 'bg-white border-slate-200 hover:bg-slate-50'
                                    }`}
                            >
                                <span className="text-3xl mb-2">{m.emoji}</span>
                                <span className="text-xs font-medium">{m.label}</span>
                            </motion.button>
                        ))}
                    </div>
                    <input
                        type="range"
                        min="1"
                        max="5"
                        value={mood}
                        onChange={(e) => setMood(parseInt(e.target.value))}
                        className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                </div>

                {/* Triggers */}
                <div className="space-y-4">
                    <label className="block text-sm font-medium text-slate-700">What's affecting you?</label>
                    <div className="flex flex-wrap gap-2">
                        {TRIGGERS.map((trigger) => (
                            <button
                                key={trigger}
                                type="button"
                                onClick={() => handleTriggerToggle(trigger)}
                                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selectedTriggers.includes(trigger)
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                            >
                                {trigger}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Journal Note */}
                <div className="space-y-4">
                    <label className="block text-sm font-medium text-slate-700">Add a note (optional)</label>
                    <textarea
                        rows={4}
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                        placeholder="What's on your mind?..."
                        className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-shadow placeholder-slate-400"
                    />
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg transition-all"
                >
                    {loading ? 'Saving...' : 'Save Entry'}
                </button>
            </form>
        </div>
    );
}
