"""
Web Snippets Generator for GitHub Activity Bot.
Generates useful JavaScript, CSS, and HTML micro-components.
"""
import random
import os

TEMPLATES = [
    {
        "filename": "debounce_throttle.js",
        "commit": "feat(web): add zero-dependency debounce and throttle implementations",
        "content": '''/**
 * Zero-dependency Debounce and Throttle Utility Functions.
 */

/**
 * Creates a debounced function that delays invoking func until after wait milliseconds
 * have elapsed since the last time the debounced function was invoked.
 */
function debounce(func, wait = 300) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), wait);
    };
}

/**
 * Creates a throttled function that only invokes func at most once per every wait milliseconds.
 */
function throttle(func, limit = 300) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

// Example usage
if (typeof window !== 'undefined') {
    const handleScroll = throttle(() => console.log('Scroll position:', window.scrollY), 200);
    window.addEventListener('scroll', handleScroll);
}
'''
    },
    {
        "filename": "event_emitter.js",
        "commit": "feat(web): implement lightweight pub/sub event emitter class",
        "content": '''/**
 * Lightweight Pub/Sub Event Emitter Class.
 */
class EventEmitter {
    constructor() {
        this.events = new Map();
    }

    on(event, listener) {
        if (!this.events.has(event)) {
            this.events.set(event, new Set());
        }
        this.events.get(event).add(listener);
        return () => this.off(event, listener);
    }

    off(event, listener) {
        if (this.events.has(event)) {
            this.events.get(event).delete(listener);
        }
    }

    emit(event, ...args) {
        if (this.events.has(event)) {
            this.events.get(event).forEach(listener => listener(...args));
        }
    }

    once(event, listener) {
        const unsubscribe = this.on(event, (...args) => {
            unsubscribe();
            listener(...args);
        });
    }
}

// Test snippet
const emitter = new EventEmitter();
const unsub = emitter.on('user:login', user => console.log('Welcome,', user));
emitter.emit('user:login', 'Alice');
unsub();
'''
    }
]


def generate_web_snippet(target_dir: str) -> tuple[str, str, str]:
    """Generates a web snippet file in target_dir and returns (rel_filepath, content, commit_message)."""
    template = random.choice(TEMPLATES)
    dest_path = os.path.join(target_dir, template["filename"])
    return dest_path, template["content"], template["commit"]
