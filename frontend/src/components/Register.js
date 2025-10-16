import React from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { validators } from '../utils';
import toast from 'react-hot-toast';
import { User, Mail, Lock, ArrowRight } from 'lucide-react';

const Register = () => {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm();

  const password = watch('password');

  const onSubmit = async (data) => {
    try {
      await registerUser(data);
      toast.success('¡Cuenta creada exitosamente!');
      navigate('/');
    } catch (error) {
      toast.error(error.message || 'Error al registrarse');
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="card">
        <div className="card-header text-center">
          <h2 className="text-2xl font-bold text-gray-900">Crear Cuenta</h2>
          <p className="text-gray-600 mt-2">
            Únete a nuestra comunidad
          </p>
        </div>
        
        <div className="card-body">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="form-group">
              <label className="form-label">
                <User size={16} className="inline mr-2" />
                Nombre de usuario
              </label>
              <input
                type="text"
                className={`form-input ${errors.username ? 'border-red-500' : ''}`}
                placeholder="tu_usuario"
                {...register('username', {
                  required: validators.required,
                  minLength: validators.minLength(3),
                  maxLength: validators.maxLength(20),
                })}
              />
              {errors.username && (
                <p className="form-error">{errors.username.message}</p>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">
                <Mail size={16} className="inline mr-2" />
                Email
              </label>
              <input
                type="email"
                className={`form-input ${errors.email ? 'border-red-500' : ''}`}
                placeholder="tu@email.com"
                {...register('email', {
                  required: validators.required,
                  validate: validators.email,
                })}
              />
              {errors.email && (
                <p className="form-error">{errors.email.message}</p>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">
                <Lock size={16} className="inline mr-2" />
                Contraseña
              </label>
              <input
                type="password"
                className={`form-input ${errors.password ? 'border-red-500' : ''}`}
                placeholder="Mínimo 6 caracteres"
                {...register('password', {
                  required: validators.required,
                  validate: validators.password,
                })}
              />
              {errors.password && (
                <p className="form-error">{errors.password.message}</p>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">
                <Lock size={16} className="inline mr-2" />
                Confirmar contraseña
              </label>
              <input
                type="password"
                className={`form-input ${errors.confirmPassword ? 'border-red-500' : ''}`}
                placeholder="Repite tu contraseña"
                {...register('confirmPassword', {
                  required: validators.required,
                  validate: (value) => 
                    value === password || 'Las contraseñas no coinciden',
                })}
              />
              {errors.confirmPassword && (
                <p className="form-error">{errors.confirmPassword.message}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="btn btn-primary btn-lg w-full"
            >
              {isSubmitting ? (
                <>
                  <div className="loading"></div>
                  Creando cuenta...
                </>
              ) : (
                <>
                  Crear Cuenta
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>
        </div>
        
        <div className="card-footer text-center">
          <p className="text-gray-600">
            ¿Ya tienes una cuenta?{' '}
            <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
              Inicia sesión aquí
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
