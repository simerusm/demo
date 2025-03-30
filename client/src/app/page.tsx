"use client"
import { useState, useEffect } from 'react';
import Head from 'next/head';
import styles from '../styles/Home.module.css';

interface Task {
  id: number; // or string, depending on your ID type
  title: string;
  completed: boolean; // or any other properties your task has
}

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`${API_URL}/api/tasks`);
        if (!response.ok) {
          throw new Error('Failed to fetch tasks');
        }
        const data = await response.json();
        setTasks(data);
        setError(null);
      } catch (err) {
        setError("Error fetching tasks. Is the backend running?");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTasks();
  }, [API_URL]);

  const addTask = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTaskTitle }),
      });

      if (!response.ok) {
        throw new Error('Failed to add task');
      }

      const newTask = await response.json();
      setTasks([...tasks, newTask]);
      setNewTaskTitle('');
    } catch (err) {
      setError('Error adding task');
      console.error(err);
    }
  };

  const toggleTaskCompleted = async (id: number, completed: boolean) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !completed }),
      });

      if (!response.ok) {
        throw new Error('Failed to update task');
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
    } catch (err) {
      setError('Error updating task');
      console.error(err);
    }
  };

  const deleteTask = async (id: number) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete task');
      }

      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError('Error deleting task');
      console.error(err);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Task Manager</title>
        <meta name="description" content="A simple task manager app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Task Manager</h1>

        {error && <p className={styles.error}>{error}</p>}

        <form onSubmit={addTask} className={styles.form}>
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Add a new task"
            className={styles.input}
          />
          <button type="submit" className={styles.button}>Add</button>
        </form>

        {isLoading ? (
          <p>Loading tasks...</p>
        ) : (
          <ul className={styles.taskList}>
            {tasks.length === 0 ? (
              <p>No tasks yet. Add one above!</p>
            ) : (
              tasks.map((task) => (
                <li key={task.id} className={styles.taskItem}>
                  <span 
                    className={`${styles.taskTitle} ${task.completed ? styles.completed : ''}`}
                    onClick={() => toggleTaskCompleted(task.id, task.completed)}
                  >
                    {task.title}
                  </span>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className={styles.deleteButton}
                  >
                    Delete
                  </button>
                </li>
              ))
            )}
          </ul>
        )}
      </main>
    </div>
  );
}