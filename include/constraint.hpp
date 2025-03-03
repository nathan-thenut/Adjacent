#include <set>

#include "entity.hpp"
#include "expression.hpp"
#include "equation_system.hpp"

#ifndef ADJACENT_CONSTRAINT_HPP
#define ADJACENT_CONSTRAINT_HPP

enum CONSTRAINT_TYPE
{
    INVALID,
    PointOn,
    PointsCoincident,
    PointCenterTriangle,
    MidPoint,
    Parallel,
    Orthogonal,
    Length,
    PointsDistance,
    HV,
    Angle,
    Diameter,
    Tangent,
    Equal
};

class Constraint;

using ConstraintPtr = std::shared_ptr<Constraint>;
using EntityPtr = std::shared_ptr<Entity>;

class Constraint
{
public:
    CONSTRAINT_TYPE type;
    std::vector<Entity*> entities;

    Constraint(CONSTRAINT_TYPE type)
        : type(type)
    {
    }

    virtual std::vector<ParamPtr> parameters() = 0;
    virtual std::vector<ExprPtr> equations() = 0;
};

class ValueConstraint : public Constraint
{
public:
    ParamPtr value = param("c_value", 0);

    bool reference = false;

    ValueConstraint(CONSTRAINT_TYPE type)
        : Constraint(type)
    {
    }

    ValueConstraint(CONSTRAINT_TYPE type, double v)
        : Constraint(type)
    {
        value->set_value(v);
    }

    void set_reference(bool value)
    {
        reference = value;
        // mark dirty
    }

    virtual bool on_satisfy()
    {
        // protected virtual bool OnSatisfy() {
        EquationSystem sys;
        sys.revert_when_not_converged = false;
        sys.add_parameter(value);
        sys.add_equations(equations());
        return sys.solve() == SolveResult::OKAY;
    }

    bool satisfy()
    {
        bool result = on_satisfy();
        if (!result)
        {
            std::cout << "satisfy failed!";  // << GetType() +;
        }
        return result;
    }

    std::vector<ParamPtr> parameters()
    {
        if (!reference)
            return {};
        else
        {
            return { value };
        }
    }

    void set_value(double v)
    {
        // label to value for helix not implemented ...
        value->set_value(v);
    }
};

class PointOnConstraint : public ValueConstraint
{
public:
    std::shared_ptr<Entity> point;
    std::shared_ptr<Entity> on;

    PointOnConstraint(std::shared_ptr<PointE> point, std::shared_ptr<Entity> on)
        : ValueConstraint::ValueConstraint(PointOn)
        , point(point)
        , on(on)
    {
        // TODO Add runtime check that point is point, and on is some other entity!
        reference = true;
        entities.push_back(point.get());
        entities.push_back(on.get());
        set_value(0.51);
        satisfy();
    }

    bool on_satisfy()
    {
        EquationSystem sys;
        auto params = parameters();
        sys.add_parameters(params);
        auto exprs = equations();
        sys.add_equations(exprs);

        double bestI = 0.0;
        double min = -1.0;
        for (double i = 0.0; i <= 1.0; i += 0.25 / 2.0)
        {
            value->set_value(i);
            sys.solve();
            double cur_value = 0;
            for (const auto& e : exprs)
            {
                cur_value += abs(e->eval());
            }
            if (min >= 0.0 && min < cur_value)
                continue;
            bestI = value->value();
            min = cur_value;
        }
        value->set_value(bestI);
        return true;
    }

    std::vector<ExprPtr> equations()
    {
        std::vector<ExprPtr> res;
        // var eq = on.PointOnInPlane(value, sketch.plane) - p;
        ExpVector equation = *on->point_on(value->expr()) - ((PointE*) point.get())->expr();
        res.push_back(equation.x);
        res.push_back(equation.y);
        // if(sketch.is3d) yield return eq.z;
        return res;
    }
};

ExprPtr angle2d(const ExpVector& d0, const ExpVector& d1, bool angle360 = false)
{
    auto nu = d1.x * d0.x + d1.y * d0.y;
    auto nv = d0.x * d1.y - d0.y * d1.x;
    if (angle360)
        return PI_E - atan2(nv, -nu);
    return atan2(nv, nu);
}

class ParallelConstraint : public Constraint
{
public:
    enum Option
    {
        Codirected,
        Antidirected
    };

    Option option_ = Option::Codirected;

    ExprPtr angle;
    std::shared_ptr<Entity> l0, l1;

    ParallelConstraint(std::shared_ptr<LineE>& l0, std::shared_ptr<LineE>& l1)
        : Constraint(CONSTRAINT_TYPE::Parallel)
        , l0(l0)
        , l1(l1)
    {
        entities.push_back(l0.get());
        entities.push_back(l1.get());
        choose_best_option();
    }

    std::vector<ExprPtr> equations()
    {
        // ExpVector d0 = l0.GetPointAtInPlane(0, sketch.plane) - l0.GetPointAtInPlane(1,
        // sketch.plane); ExpVector d1 = l1.GetPointAtInPlane(0, sketch.plane) -
        // l1.GetPointAtInPlane(1, sketch.plane);
        ExpVector d0 = *l0->point_on(zero) - *l0->point_on(one);
        ExpVector d1 = *l1->point_on(zero) - *l1->point_on(one);
        // ExprPtr angle = sketch.is3d ? ConstraintExp.angle3d(d0, d1) : ConstraintExp.angle2d(d0,
        // d1);
        if (!angle)
        {
            angle = angle2d(d0, d1);
        }
        switch (option_)
        {
            case Option::Codirected:
                return { angle };
            case Option::Antidirected:
                return { abs(angle) - PI_E };
        }
        throw std::runtime_error("unhandled option");
    }

    void choose_best_option()
    {
        double min_value = -1.0;
        int best_option = 0;

        for (int i = 0; i < 2; i++)
        {
            auto exprs = equations();
            double cur_value = 0.0;
            for (const auto& el : exprs)
            {
                cur_value += abs(el->eval());
            }
            std::clog << "check option " << i << " (min: " << min_value << ", cur: " << cur_value
                      << ")\n";

            if (min_value < 0.0 || cur_value < min_value)
            {
                min_value = cur_value;
                best_option = i;
                option_ = (Option) i;
            }
        }
    }

    std::vector<ParamPtr> parameters()
    {
        return {};
    }
};


class OrthogonalConstraint : public Constraint
{
public:
    std::shared_ptr<Entity> l0, l1;

    OrthogonalConstraint(std::shared_ptr<LineE>& l0, std::shared_ptr<LineE>& l1)
        : Constraint(CONSTRAINT_TYPE::Orthogonal)
        , l0(l0)
        , l1(l1)
    {
        entities.push_back(l0.get());
        entities.push_back(l1.get());
    }

    std::vector<ExprPtr> equations()
    {
        ExpVector d0 = *l0->point_on(zero) - *l0->point_on(one);
        ExpVector d1 = *l1->point_on(zero) - *l1->point_on(one);
        return { d0.x * d1.x + d0.y * d1.y };
    }

    std::vector<ParamPtr> parameters()
    {
        return {};
    }
};

class LengthConstraint : public ValueConstraint
{
public:
    std::shared_ptr<Entity> entity;

    LengthConstraint(std::shared_ptr<Entity> e, double l)
        : ValueConstraint(CONSTRAINT_TYPE::Length, l)
        , entity(e)
    {
        entities.push_back(e.get());
        satisfy();  // does this make sense here?
        value->set_value(l);
    }

    std::vector<ExprPtr> equations()
    {
        return { entity->length() - value->expr() };
    }
};


class EqualConstraint : public ValueConstraint
{
public:
    std::shared_ptr<Entity> e1, e2;

    EqualConstraint(std::shared_ptr<LineE> e1, std::shared_ptr<LineE> e2)
        : ValueConstraint(CONSTRAINT_TYPE::Equal, 1)
        , e1(e1)
        , e2(e2)
    {
        entities.push_back(e1.get());
        entities.push_back(e2.get());
        satisfy();  // does this make sense here?
        value->set_value(1);
    }

    EqualConstraint(std::shared_ptr<LineE> e1, std::shared_ptr<LineE> e2, double factor)
        : ValueConstraint(CONSTRAINT_TYPE::Equal, factor)
        , e1(e1)
        , e2(e2)
    {
        entities.push_back(e1.get());
        entities.push_back(e2.get());
        satisfy();  // does this make sense here?
        value->set_value(factor);
    }

    std::vector<ExprPtr> equations()
    {
        return { e1->length() - e2->length() * value->expr() };
    }
};

class PointsCoincidentConstraint : public Constraint
{
public:
    std::shared_ptr<PointE> p0, p1;

    PointsCoincidentConstraint(std::shared_ptr<PointE>& p0, std::shared_ptr<PointE>& p1)
        : Constraint(CONSTRAINT_TYPE::PointsCoincident)
        , p0(p0)
        , p1(p1)
    {
        entities.push_back(p0.get());
        entities.push_back(p1.get());
    }

    std::vector<ExprPtr> equations()
    {
        // var pe0 = p0.GetPointAtInPlane(0, sketch.plane);
        // var pe1 = p1.GetPointAtInPlane(0, sketch.plane);

        return std::vector<ExprPtr>(
            { p0->x->expr() - p1->x->expr(), p0->y->expr() - p1->y->expr() });
        // if 3d
        // if(sketch.is3d) yield return pe0.z - pe1.z;
    }

    std::vector<ParamPtr> parameters()
    {
        return {};
    }

    std::shared_ptr<PointE>& get_other_point(const std::shared_ptr<PointE>& p)
    {
        if (p0 == p)
            return p1;
        return p0;
    }
};


class MidPointConstraint : public ValueConstraint
{
public:
    std::shared_ptr<PointE> p0, p1, p2;

    MidPointConstraint(std::shared_ptr<PointE> p0, std::shared_ptr<PointE> p1,
                       std::shared_ptr<PointE> p2)
        : ValueConstraint(CONSTRAINT_TYPE::MidPoint, 1)
        , p0(p0)
        , p1(p1)
        , p2(p2)
    {
        entities.push_back(p0.get());
        entities.push_back(p1.get());
        entities.push_back(p2.get());
        satisfy();
        value->set_value(2);
    }

    std::vector<ExprPtr> equations()
    {
        return std::vector<ExprPtr>({
            p0->x->expr() + p1->x->expr() - value->expr() * p2->x->expr(),
            p0->y->expr() + p1->y->expr() - value->expr() * p2->y->expr(),
        });
    }
};

class PointCenterTriangleConstraint : public ValueConstraint
{
public:
    std::shared_ptr<PointE> p0, p1, p2, p3;

    PointCenterTriangleConstraint(std::shared_ptr<PointE>& p0, std::shared_ptr<PointE>& p1,
                                  std::shared_ptr<PointE>& p2, std::shared_ptr<PointE>& p3)
        : ValueConstraint(CONSTRAINT_TYPE::PointCenterTriangle, 1)
        , p0(p0)
        , p1(p1)
        , p2(p2)
        , p3(p3)
    {
        entities.push_back(p0.get());
        entities.push_back(p1.get());
        entities.push_back(p2.get());
        entities.push_back(p3.get());
        satisfy();
        value->set_value(3);
    }

    std::vector<ExprPtr> equations()
    {
        return std::vector<ExprPtr>({
            p0->x->expr() + p1->x->expr() + p2->x->expr() - value->expr() * p3->x->expr(),
            p0->y->expr() + p1->y->expr() + p2->y->expr() - value->expr() * p3->y->expr(),
        });
    }
};


class PointsDistanceConstraint : public ValueConstraint
{
public:
    EntityPtr p0, p1;

    PointsDistanceConstraint(const std::shared_ptr<PointE>& p0, const std::shared_ptr<PointE>& p1,
                             double d)
        : ValueConstraint(CONSTRAINT_TYPE::PointsDistance, d)
        , p0(p0)
        , p1(p1)
    {
        entities.push_back(p0.get());
        entities.push_back(p1.get());
        satisfy();
        value->set_value(d);
    }

    PointsDistanceConstraint(const std::shared_ptr<LineE>& line, double d)
        : ValueConstraint(CONSTRAINT_TYPE::PointsDistance, d)
        , p0(line)
        , p1(nullptr)
    {
        entities.push_back(line.get());
        satisfy();
        value->set_value(d);
    }

    std::vector<ExprPtr> equations()
    {
        return std::vector<ExprPtr>({ // TODO caching
                                      (get_point(1) - get_point(0)).magnitude() - value->expr() });
    }

    ExpVector get_point(double i)
    {
        if (p1 == nullptr)
        {
            return i ? dynamic_cast<LineE*>(p0.get())->source().expr()
                     : dynamic_cast<LineE*>(p0.get())->target().expr();
        }
        else
        {
            return i ? dynamic_cast<PointE*>(p0.get())->expr()
                     : dynamic_cast<PointE*>(p1.get())->expr();
        }
    }
};

enum HVOrientation
{
    OX,
    OY,
    // OZ
};

class HVConstraint : public Constraint
{
public:
    PointE* p0;
    PointE* p1;

    HVOrientation orientation = HVOrientation::OX;

    HVConstraint(std::shared_ptr<PointE> p0, std::shared_ptr<PointE> p1, HVOrientation o)
        : Constraint(CONSTRAINT_TYPE::HV)
        , p0(p0.get())
        , p1(p1.get())
        , orientation(o)
    {
        entities.push_back(p0.get());
        entities.push_back(p1.get());
    }

    HVConstraint(std::shared_ptr<LineE> line, HVOrientation o)
        : Constraint(CONSTRAINT_TYPE::HV)
        , p0(&(line.get())->source())
        , p1(&(line.get())->target())
        , orientation(o)
    {
        entities.push_back(line.get());
    }

    std::vector<ExprPtr> equations()
    {
        ExprPtr exp;
        switch (orientation)
        {
            case HVOrientation::OX:
                exp = p0->x->expr() - p1->x->expr();
                break;
            case HVOrientation::OY:
                exp = p0->y->expr() - p1->y->expr();
                break;
                // case HVOrientation::OZ: exp = p0->z->expr() - p1->z->expr(); break;
        }

        return std::vector<ExprPtr>({ exp });
    }

    std::vector<ParamPtr> parameters()
    {
        return {};
    }
};

template <class T>
T sgn(const T& x)
{
    return (x < T(0)) ? T(-1) : T(+1);
}

class AngleConstraint : public ValueConstraint
{
public:
    bool supplementary = false;
    // AngleConstraint(PointE)

    // AngleConstraint(Arc);

    AngleConstraint(std::shared_ptr<LineE>& l0, std::shared_ptr<LineE>& l1, double angle)
        : ValueConstraint(CONSTRAINT_TYPE::Angle, angle)
    {
        entities.push_back(l0.get());
        entities.push_back(l1.get());
        // satisfy();
        value->set_value(angle);
    }

    std::vector<ExprPtr> equations()
    {
        std::array<ExpVector, 4> pts;
        if (std::abs(value->value()) > M_PI_2)
        {
            // If we have values > pi/2 it's better to flip the computation of the angle
            // so that atan2 doesn't go too high (becomes unstable for solving at around 0.92 * PI)
            // atan2 is only defined between 0 and +/- PI
            // so we flip the line segment, and use the negative angle instead.
            supplementary = true;
            value->set_value(-(sgn(value->value()) * M_PI - value->value()));
            pts = get_points(true);
        }
        else
        {
            // value->set_value(value->value());
            pts = get_points(true);
        }

        auto d0 = pts[0] - pts[1];
        auto d1 = pts[2] - pts[3];
        // bool angle360 = is_arc?
        bool angle360 = false;
        // Exp angle = sketch.is3d
        ExprPtr angle = angle2d(d0, d1, angle360);
        return { angle - value->expr() };
    }

    std::array<ExpVector, 4> get_points(bool swap)
    {
        std::array<ExpVector, 4> res;

        if (!swap)  // points
        {
            for (int i = 0; i < 4; ++i)
            {
                res[i] = dynamic_cast<PointE*>(entities[i])->expr();
            }
        }
        else if (swap)  // line
        {
            LineE* l0 = dynamic_cast<LineE*>(entities[0]);
            res[0] = *l0->point_on(zero);
            res[1] = *l0->point_on(one);
            LineE* l1 = dynamic_cast<LineE*>(entities[1]);
            res[2] = *l1->point_on(zero);
            res[3] = *l1->point_on(one);
            if (supplementary)
            {
                // Swap direction of l1
                std::swap(res[2], res[3]);
            }
        }

        return res;
    }
};

class DiameterConstraint : public ValueConstraint
{
public:
    // bool showAsRadius = false;
    EntityPtr e;

    DiameterConstraint(EntityPtr& entity, double diameter)
        : ValueConstraint(CONSTRAINT_TYPE::Diameter, diameter)
        , e(entity)
    {
        // showAsRadius = (c.type == IEntityType.Arc);
        entities.push_back(entity.get());
        // satisfy();
        value->set_value(diameter);
    }

    std::vector<ExprPtr> equations()
    {
        return { e->radius() * two - value->expr() };
    }
};

class TangentConstraint : public Constraint
{
public:
    enum Option
    {
        Codirected,
        Antidirected
    };

    Option _option = Option::Codirected;

    void choose_best_option()
    {
        double min_value = -1.0;
        int best_option = 0;

        for (int i = 0; i < 2; i++)
        {
            auto exprs = equations();
            double cur_value = 0.0;
            for (const auto& el : exprs)
            {
                cur_value += abs(el->eval());
            }
            std::clog << "check option " << i << " (min: " << min_value << ", cur: " << cur_value
                      << ")\n";

            if (min_value < 0.0 || cur_value < min_value)
            {
                min_value = cur_value;
                best_option = i;
                _option = (Option) i;
            }
        }
    }

    ParamPtr t0 = param("t0", 0.0);
    ParamPtr t1 = param("t1", 0.0);

    bool add_angle = true;

    TangentConstraint(std::shared_ptr<CircleE>& c, std::shared_ptr<LineE>& l)
        : Constraint(CONSTRAINT_TYPE::Tangent)
    {
        // make sure that e1 is circular entity?
        entities.push_back(c.get());
        entities.push_back(l.get());

        choose_best_option();
    }

    bool is_coincident(double& tv0, double& tv1, ExprPtr& c, ParamPtr& p)
    {
        auto* l0 = entities[0];
        auto* l1 = entities[1];

        auto* s0 = dynamic_cast<SegmentaryEntity*>(l0);
        auto* s1 = dynamic_cast<SegmentaryEntity*>(l1);

        // For the is_coincident_with_curve query we need to have access to all constraints to query
        // wether there is a coincident with ... constraint already

        // if(s0 != nullptr && s1 != nullptr) {
        //    if (s0->begin->IsCoincidentWith(s1.begin))   { tv0 = 0.0; tv1 = 0.0; return true; }
        //     if (s0.begin.IsCoincidentWith(s1.end))      { tv0 = 0.0; tv1 = 1.0; return true; }
        //     if (s0.end.IsCoincidentWith(s1.begin))      { tv0 = 1.0; tv1 = 0.0; return true; }
        //     if (s0.end.IsCoincidentWith(s1.end))        { tv0 = 1.0; tv1 = 1.0; return true; }
        // }
        // if(s0 != nullptr)
        // {
        //     PointOn pOn = null;
        //     if (s0.source().IsCoincidentWithCurve(l1, ref pOn))
        //     {
        //         tv0 = 0.0;
        //         p = t1;
        //         c = new Exp(t1) - pOn.GetValueParam();
        //         return true;
        //     }
        //     if (s0.end.IsCoincidentWithCurve(l1, ref pOn))
        //     {
        //         tv0 = 1.0;
        //         p = t1;
        //         c = new Exp(t1) - pOn.GetValueParam();
        //         return true;
        //     }
        // }
        // if(s1 != null) {
        //     PointOn pOn = null;
        //     if(s1.begin.IsCoincidentWithCurve(l0, ref pOn)) { p = t0; c = new Exp(t0) -
        //     pOn.GetValueParam(); tv1 = 0.0; return true; } if(s1.end.IsCoincidentWithCurve(l0,
        //     ref pOn))   { p = t0; c = new Exp(t0) - pOn.GetValueParam(); tv1 = 1.0; return true;
        //     }
        // }
        return false;
    }

    std::vector<ParamPtr> parameters()
    {
        double tv0 = 0.0;
        double tv1 = 0.0;
        ExprPtr c = nullptr;
        ParamPtr p = nullptr;

        if (is_coincident(tv0, tv1, c, p) == false)
        {
            return { t0, t1 };
        }
        else
        {
            if (p != nullptr)
            {
                return { p };
            }
        }
        return {};
    }

    std::vector<ExprPtr> equations()
    {
        // select point on circle (t0) and on line (t1),
        // force them to overlap and have equal tangent angle

        std::vector<ExprPtr> res;
        auto* l0 = entities[0];
        auto* l1 = entities[1];

        ExpVectorPtr dir0 = l0->tangent_at(t0->expr());
        ExpVectorPtr dir1 = l1->tangent_at(t1->expr());

        // dir0 = l0.plane.DirFromPlane(dir0);
        // dir0 = sketch.plane.DirToPlane(dir0);

        // dir1 = l1.plane.DirFromPlane(dir1);
        // dir1 = sketch.plane.DirToPlane(dir1);

        if (add_angle)
        {
            // Exp angle = sketch.is3d ? ConstraintExp.angle3d(dir0, dir1) :
            // ConstraintExp.angle2d(dir0, dir1);
            auto angle = angle2d(*dir0, *dir1);
            switch (_option)
            {
                case Option::Codirected:
                    res.push_back(angle);
                    break;
                case Option::Antidirected:
                    res.push_back(abs(angle) - PI_E);
                    break;
            }
        }

        double tv0 = t0->value();
        double tv1 = t1->value();

        ExprPtr c;
        ParamPtr p;

        // if we already have a coincident constraint on P and the Curve C:
        if (is_coincident(tv0, tv1, c, p))
        {
            t0->set_value(tv0);
            t1->set_value(tv1);
            if (c != nullptr)
                res.push_back(c);
        }
        else
        {
            // var eq = l1.PointOnInPlane(t1, sketch.plane) - l0.PointOnInPlane(t0, sketch.plane);
            auto eq = *l1->point_on(t1->expr()) - *l0->point_on(t0->expr());
            res.push_back(eq.x);
            res.push_back(eq.y);
            // if(sketch.is3d) res.push_back(eq.z);
        }
        return res;
    }
};

class Sketch
{
public:
    bool constraintsTopologyChanged = true;
    bool constraintsChanged = true;
    bool entitiesChanged = true;
    bool loopsChanged = true;
    bool topologyChanged = true;
    bool supressSolve;
    EquationSystem sys;

    std::set<EntityPtr> entities;
    std::set<ExprPtr> expressions;
    std::set<ConstraintPtr> constraints;

    void add_entity(const EntityPtr& e)
    {
        if (entities.find(e) != entities.end())
            return;
        entities.insert(e);
        mark_dirty(/*topo*/ true, /*constraints*/ false, /*entities*/ true, /*loops*/ false);
    }

    void remove_entity(const EntityPtr& e)
    {
        if (entities.find(e) == entities.end())
            return;
        entities.erase(e);
        mark_dirty(/*topo*/ true, /*constraints*/ false, /*entities*/ true, /*loops*/ false);
    }

    void mark_dirty(bool topo, bool constraints, bool entities, bool loops)
    {
        topologyChanged = topologyChanged || topo;
        constraintsChanged = constraintsChanged || constraints;
        constraintsTopologyChanged = constraintsTopologyChanged || constraints;
        entitiesChanged = entitiesChanged || entities;
        loopsChanged = loopsChanged || loops;
    }

    void add_constraint(const ConstraintPtr& c)
    {
        if (constraints.find(c) != constraints.end())
            return;
        constraints.insert(c);
        mark_dirty(/*topo*/ c->type == PointsCoincident,
                   /*constraints*/ true,
                   /*entities*/ false,
                   /*loops*/ false);
        constraintsTopologyChanged = true;
    }

    void remove_constraint(const ConstraintPtr& c)
    {
        if (constraints.find(c) == constraints.end())
            return;
        constraints.erase(c);
        mark_dirty(/*topo*/ c->type == PointsCoincident,
                   /*constraints*/ true,
                   /*entities*/ false,
                   /*loops*/ false);
        constraintsTopologyChanged = true;
    }

    void add_expression(const ExprPtr& e)
    {
        if (expressions.find(e) != expressions.end())
            return;
        expressions.insert(e);
        mark_dirty(/*topo*/ true, /*constraints*/ false, /*entities*/ false, /*loops*/ false);
        constraintsTopologyChanged = true;  // unsure?
    }

    void remove_expression(const ExprPtr& e)
    {
        if (expressions.find(e) == expressions.end())
            return;
        expressions.erase(e);
        mark_dirty(/*topo*/ true, /*constraints*/ false, /*entities*/ false, /*loops*/ false);
        constraintsTopologyChanged = true;  // unsure?
    }

    void add_expressionVector(const ExpVectorPtr& e)
    {
        if (expressions.find(e->x) != expressions.end())
            return;
        expressions.insert(e->x);
        if (expressions.find(e->y) != expressions.end())
            return;
        expressions.insert(e->y);
        if (expressions.find(e->z) != expressions.end())
            return;
        expressions.insert(e->z);
        mark_dirty(/*topo*/ true, /*constraints*/ false, /*entities*/ false, /*loops*/ false);
        constraintsTopologyChanged = true;  // unsure?
    }

    void remove_expressionVector(const ExpVectorPtr& e)
    {
        if (expressions.find(e->x) == expressions.end())
            return;
        expressions.erase(e->x);
        if (expressions.find(e->y) == expressions.end())
            return;
        expressions.erase(e->y);
        if (expressions.find(e->z) == expressions.end())
            return;
        expressions.erase(e->z);
        mark_dirty(/*topo*/ true, /*constraints*/ false, /*entities*/ false, /*loops*/ false);
        constraintsTopologyChanged = true;  // unsure?
    }

    bool is_dirty() const
    {
        return constraintsTopologyChanged || constraintsChanged || entitiesChanged || loopsChanged
               || topologyChanged;
    }

    bool is_entities_changed() const
    {
        return entitiesChanged;
    }

    bool is_constraints_changed() const
    {
        return constraintsChanged;
    }
    bool is_topology_changed() const
    {
        return topologyChanged;
    }

    bool is_using_linear_program() const
    {
        return sys.use_linear_program;
    }

    void use_linear_program(bool use_lp)
    {
        sys.use_linear_program = use_lp;
    }

    int update()
    {
        if (is_constraints_changed() || is_entities_changed())
        {
            supressSolve = false;
        }
        if (is_topology_changed() || constraintsTopologyChanged)
        {
            sys.clear();
            generate_equations(sys);
        }
        auto res = (!supressSolve || sys.has_dragged()) ? sys.solve() : DIDNT_CONVERGE;
        if (res == DIDNT_CONVERGE)
        {
            supressSolve = true;
        }
        topologyChanged = false;
        constraintsChanged = false;
        constraintsTopologyChanged = false;
        entitiesChanged = false;
        loopsChanged = false;
        return sys.counted_steps;
    }

    void generate_equations(EquationSystem& system)
    {
        for (const auto& e : expressions)
        {
            system.add_equation(e);
        }
        for (const auto& en : entities)
        {
            system.add_parameters(en->parameters());
            // system.add_equations(en->equations());
        }
        for (const auto& c : constraints)
        {
            system.add_parameters(c->parameters());
            system.add_equations(c->equations());
        }
    }
};

#endif
