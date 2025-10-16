import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { usePosts } from '../hooks/usePosts';
import { validators } from '../utils';
import toast from 'react-hot-toast';
import { FileText, ArrowLeft, Send } from 'lucide-react';

const CreatePost = () => {
  const { createPost } = usePosts();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  const onSubmit = async (data) => {
    try {
      await createPost(data);
      navigate('/');
    } catch (error) {
      // Error ya manejado en el hook
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <button
          onClick={() => navigate('/')}
          className="btn btn-ghost mb-4"
        >
          <ArrowLeft size={16} />
          Volver al inicio
        </button>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Crear Nuevo Post
        </h1>
        <p className="text-gray-600">
          Comparte tus ideas y experiencias con la comunidad
        </p>
      </div>

      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="form-group">
              <label className="form-label">
                <FileText size={16} className="inline mr-2" />
                Título del post
              </label>
              <input
                type="text"
                className={`form-input ${errors.title ? 'border-red-500' : ''}`}
                placeholder="Escribe un título atractivo..."
                {...register('title', {
                  required: validators.required,
                  minLength: validators.minLength(5),
                  maxLength: validators.maxLength(200),
                })}
              />
              {errors.title && (
                <p className="form-error">{errors.title.message}</p>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">
                Contenido
              </label>
              <textarea
                className={`form-textarea ${errors.content ? 'border-red-500' : ''}`}
                placeholder="Escribe tu historia, ideas o experiencias aquí..."
                rows={12}
                {...register('content', {
                  required: validators.required,
                  minLength: validators.minLength(10),
                  maxLength: validators.maxLength(5000),
                })}
              />
              {errors.content && (
                <p className="form-error">{errors.content.message}</p>
              )}
              <p className="text-sm text-gray-500 mt-1">
                Mínimo 10 caracteres, máximo 5000 caracteres
              </p>
            </div>

            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="btn btn-secondary flex-1"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="btn btn-primary flex-1"
              >
                {isSubmitting ? (
                  <>
                    <div className="loading"></div>
                    Publicando...
                  </>
                ) : (
                  <>
                    <Send size={16} />
                    Publicar Post
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CreatePost;
