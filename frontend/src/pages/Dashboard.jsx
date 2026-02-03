import { motion } from 'framer-motion'
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/20/solid'

const stats = [
    { name: 'Current Streak', stat: '5 Days', icon: '🔥', change: '+2', changeType: 'increase' },
    { name: 'Average Mood', stat: '7.2', icon: '😊', change: '+0.5', changeType: 'increase' },
    { name: 'Entries This Week', stat: '12', icon: '📝', change: '-2', changeType: 'decrease' },
]

export default function Dashboard() {
    return (
        <div className="space-y-8">
            {/* Stats Overview */}
            <div>
                <h3 className="text-base font-semibold leading-6 text-slate-900">Overview</h3>
                <dl className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
                    {stats.map((item) => (
                        <motion.div
                            key={item.name}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6"
                        >
                            <dt className="truncate text-sm font-medium text-slate-500">{item.name}</dt>
                            <dd className="mt-1 flex items-baseline justify-between md:block lg:flex">
                                <div className="flex items-baseline text-2xl font-semibold text-slate-900">
                                    <span className="mr-2">{item.icon}</span>
                                    {item.stat}
                                </div>

                                <div
                                    className={`inline-flex items-baseline rounded-full px-2.5 py-0.5 text-sm font-medium md:mt-2 lg:mt-0 ${item.changeType === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                        }`}
                                >
                                    {item.changeType === 'increase' ? (
                                        <ArrowUpIcon
                                            className="-ml-1 mr-0.5 h-4 w-4 flex-shrink-0 self-center text-green-500"
                                            aria-hidden="true"
                                        />
                                    ) : (
                                        <ArrowDownIcon
                                            className="-ml-1 mr-0.5 h-4 w-4 flex-shrink-0 self-center text-red-500"
                                            aria-hidden="true"
                                        />
                                    )}
                                    {item.change}
                                </div>
                            </dd>
                        </motion.div>
                    ))}
                </dl>
            </div>

            {/* Mood Chart Placeholder */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="bg-white p-6 rounded-lg shadow"
            >
                <h3 className="text-lg font-medium text-slate-900 mb-4">Weekly Mood Trend</h3>
                <div className="h-64 flex items-center justify-center bg-slate-50 rounded-lg border-2 border-dashed border-slate-200 text-slate-400">
                    Chart Component Coming Soon
                </div>
            </motion.div>

            {/* Recent Entries */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="bg-white shadow sm:rounded-md"
            >
                <div className="border-b border-slate-200 px-4 py-5 sm:px-6">
                    <h3 className="text-base font-semibold leading-6 text-slate-900">Recent Entries</h3>
                </div>
                <ul role="list" className="divide-y divide-slate-200">
                    {[1, 2, 3].map((item) => (
                        <li key={item} className="px-4 py-4 sm:px-6 hover:bg-slate-50 transition-colors">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <div className="flex-shrink-0">
                                        <span className="text-2xl">😊</span>
                                    </div>
                                    <div className="ml-4">
                                        <p className="truncate text-sm font-medium text-slate-900">Feeling great today!</p>
                                        <p className="text-xs text-slate-500">Just now</p>
                                    </div>
                                </div>
                                <div>
                                    <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
                                        Score: 8/10
                                    </span>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </motion.div>
        </div>
    )
}
