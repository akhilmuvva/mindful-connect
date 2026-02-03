import { motion } from 'framer-motion';

export default function Loading() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[50vh]">
            <motion.div
                animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.5, 1, 0.5],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="relative flex items-center justify-center"
            >
                <div className="absolute w-16 h-16 rounded-full bg-blue-400 opacity-20 blur-xl"></div>
                <img
                    src="https://img.icons8.com/color/96/000000/lotus.png"
                    alt="Loading..."
                    className="w-12 h-12 relative z-10"
                />
            </motion.div>
            <p className="mt-4 text-slate-500 text-sm font-medium">Breathe in...</p>
        </div>
    );
}
